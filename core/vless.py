import asyncio
import socket
import time
import logging
from typing import Callable, Awaitable
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger("Midoxy")

RELAY_BUF = 256 * 1024          # 256KB buffer chunk
SOCK_BUF = 512 * 1024           # 512KB OS socket buffer to avoid bufferbloat
WRITE_HIGH_WATER = 128 * 1024   # Drain threshold to minimize latency

QUOTA_MIN_BATCH = 32 * 1024
QUOTA_MAX_BATCH = 2 * 1024 * 1024
QUOTA_START_BATCH = 128 * 1024
QUOTA_CHECK_INTERVAL = 0.25


def tune_socket(writer: asyncio.StreamWriter):
    """Fine-tune TCP socket options for high-throughput and resilient mobile connections."""
    try:
        sock = writer.transport.get_extra_info("socket")
        if sock is None:
            return
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SOCK_BUF)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, SOCK_BUF)
        if hasattr(socket, "TCP_QUICKACK"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
        if hasattr(socket, "TCP_USER_TIMEOUT"):
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, 20000)  # 20s
    except Exception as exc:
        logger.debug(f"Socket tuning warning: {exc}")


class QuotaGate:
    """Adaptive quota gate using EWMA rate estimation to avoid frequent lock contention."""
    __slots__ = ("uuid", "pending", "last_check", "ok", "batch_bytes", "rate_ewma", "check_cb")

    def __init__(self, uuid: str, check_cb: Callable[[str, int], Awaitable[bool]]):
        self.uuid = uuid
        self.check_cb = check_cb
        self.pending = 0
        self.last_check = time.monotonic()
        self.ok = True
        self.batch_bytes = QUOTA_START_BATCH
        self.rate_ewma = 0.0

    async def add(self, nbytes: int) -> bool:
        if not self.ok:
            return False
        self.pending += nbytes
        now = time.monotonic()
        elapsed = now - self.last_check
        if self.pending >= self.batch_bytes or elapsed >= QUOTA_CHECK_INTERVAL:
            flush, self.pending = self.pending, 0
            if elapsed > 0:
                inst_rate = flush / elapsed
                self.rate_ewma = inst_rate if self.rate_ewma == 0 else (0.7 * self.rate_ewma + 0.3 * inst_rate)
                target = int(self.rate_ewma * QUOTA_CHECK_INTERVAL)
                self.batch_bytes = max(QUOTA_MIN_BATCH, min(QUOTA_MAX_BATCH, target or QUOTA_MIN_BATCH))
            self.last_check = now
            try:
                self.ok = await self.check_cb(self.uuid, flush)
            except Exception as exc:
                logger.error(f"QuotaGate check error {self.uuid[:8]}: {exc}")
                self.ok = False
            return self.ok
        return True

    async def flush(self) -> bool:
        if self.pending:
            flush, self.pending = self.pending, 0
            try:
                self.ok = self.ok and await self.check_cb(self.uuid, flush)
            except Exception as exc:
                logger.error(f"QuotaGate flush error {self.uuid[:8]}: {exc}")
                self.ok = False
        return self.ok


def get_client_ip(ws: WebSocket) -> str:
    fwd = ws.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = ws.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return ws.client.host if ws.client else "unknown"


async def parse_vless_header(chunk: bytes):
    if len(chunk) < 24:
        raise ValueError("Payload chunk too small for VLESS protocol")
    pos = 1  # version (1 byte)
    pos += 16  # UUID (16 bytes)
    addon_len = chunk[pos]
    pos += 1 + addon_len
    command = chunk[pos]
    pos += 1
    port = int.from_bytes(chunk[pos:pos+2], "big")
    pos += 2
    addr_type = chunk[pos]
    pos += 1

    if addr_type == 1:  # IPv4
        address = ".".join(str(b) for b in chunk[pos:pos+4])
        pos += 4
    elif addr_type == 2:  # Domain
        dlen = chunk[pos]
        pos += 1
        address = chunk[pos:pos+dlen].decode("utf-8", errors="ignore")
        pos += dlen
    elif addr_type == 3:  # IPv6
        ab = chunk[pos:pos+16]
        pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"Unsupported address type: {addr_type}")

    return command, address, port, chunk[pos:]


async def relay_ws_to_tcp(
    ws: WebSocket,
    writer: asyncio.StreamWriter,
    uid: str,
    conn: dict,
    check_cb: Callable[[str, int], Awaitable[bool]],
    on_traffic_cb: Callable[[int], None],
):
    gate = QuotaGate(uid, check_cb)
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if not await gate.add(len(data)):
                await ws.close(code=1008, reason="quota_exceeded")
                break
            conn["bytes"] += len(data)
            on_traffic_cb(len(data))
            writer.write(data)
            if writer.transport.get_write_buffer_size() > WRITE_HIGH_WATER:
                await writer.drain()
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        await gate.flush()
        try:
            writer.write_eof()
        except Exception:
            pass


async def relay_tcp_to_ws(
    ws: WebSocket,
    reader: asyncio.StreamReader,
    uid: str,
    conn: dict,
    check_cb: Callable[[str, int], Awaitable[bool]],
    on_traffic_cb: Callable[[int], None],
):
    gate = QuotaGate(uid, check_cb)
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await gate.add(len(data)):
                await ws.close(code=1008, reason="quota_exceeded")
                break
            conn["bytes"] += len(data)
            on_traffic_cb(len(data))
            # VLESS protocol requires 2 zero bytes prefix on the first response frame
            payload = (b"\x00\x00" + data) if first else data
            first = False
            await ws.send_bytes(payload)
    except Exception:
        pass
    finally:
        await gate.flush()

