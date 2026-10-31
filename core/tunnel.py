import asyncio
import secrets
import logging
from datetime import datetime, timezone
from fastapi import WebSocket, WebSocketDisconnect

from core.manager import (
    LINKS, LINKS_LOCK, CONNECTIONS, is_link_allowed,
    check_and_use, track_request, track_error, save_state_debounced
)
from core.vless import (
    tune_socket, get_client_ip, parse_vless_header,
    relay_ws_to_tcp, relay_tcp_to_ws
)

logger = logging.getLogger("Midoxy")


async def vless_ws_handler(ws: WebSocket, uuid: str):
    await ws.accept()

    async with LINKS_LOCK:
        link = LINKS.get(uuid)

    if not is_link_allowed(link):
        logger.warning(f"Connection rejected for uuid={uuid[:8]} (disabled or quota exceeded)")
        await ws.close(code=1008, reason="not_authorized")
        return

    client_ip = get_client_ip(ws)
    conn_id = secrets.token_urlsafe(6)
    conn = {
        "uuid": uuid,
        "ip": client_ip,
        "connected_at": datetime.now(timezone.utc).isoformat(),
        "bytes": 0,
    }
    CONNECTIONS[conn_id] = conn
    logger.info(f"Connected: [{conn_id}] uuid={uuid[:8]} from {client_ip} | Active: {len(CONNECTIONS)}")

    writer = None
    try:
        # Receive first packet containing VLESS handshake
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        command, address, port, payload = await parse_vless_header(first_chunk)

        # Check quota for handshake packet
        if not await check_and_use(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota_exceeded")
            return

        track_request()
        conn["bytes"] += len(first_chunk)
        logger.info(f"Relay [{conn_id}] -> {address}:{port}")

        # Connect out to destination
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port),
            timeout=10.0
        )
        tune_socket(writer)

        if payload:
            writer.write(payload)
            await writer.drain()

        def on_traffic(n: int):
            pass

        # Bi-directional stream
        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, uuid, conn, check_and_use, on_traffic)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, uuid, conn, check_and_use, on_traffic)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        asyncio.create_task(save_state_debounced())

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        track_error("Handshake / connection timeout")
    except Exception as exc:
        track_error(f"WS error [{conn_id}]: {exc}")
        logger.error(f"WS tunnel exception: {exc}")
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        CONNECTIONS.pop(conn_id, None)
        logger.info(f"Disconnected: [{conn_id}] | Active: {len(CONNECTIONS)}")

