# Midoxy

<div align="center">

<h3>High-Throughput Asynchronous Edge Stream Gateway & Telemetry Core</h3>

<p>A production-ready, low-latency stream relay and event microservice optimized for zero-configuration cloud deployment on <strong>Seenode</strong>.</p>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Deployed on Seenode](https://img.shields.io/badge/Deploy-Seenode-0B0D0E?style=flat-square)](https://seenode.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg?style=flat-square)](./LICENSE)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Seenode Cloud Deployment Guide](#-seenode-cloud-deployment-guide)
- [Local Development](#-local-development)
- [Environment Configuration](#-environment-configuration)
- [Health & Observability](#-health--observability)
- [License & Maintainer](#-license--maintainer)

---

## ⚡ Overview

**Midoxy** is a modern, high-performance edge streaming relay designed for asynchronous bi-directional socket multiplexing. Built with **FastAPI**, **uvloop**, and **AsyncIO**, it offers enterprise-grade I/O throughput with minimal memory footprint and zero external database requirements.

Designed specifically for cloud PaaS environments like **Seenode**, Midoxy features automatic environment detection, dynamic reverse proxy host mapping, atomic disk state snapshots, and an embedded administrative console.

---

## 🏗 Architecture

```
┌─────────────────┐       HTTPS / WSS        ┌────────────────────────────┐
│ Incoming Client │ ───────────────────────► │ Seenode Ingress & TLS Edge │
└─────────────────┘                          └─────────────┬──────────────┘
                                                           │ Internal Port $PORT
                                                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                             MIDOXY CORE                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  • GET /                ──► Public Decoy Developer Portfolio             │
│  • GET /health          ──► Seenode Zero-Downtime Health Monitor        │
│  • GET /login           ──► Administrative Authentication Console       │
│  • GET /dashboard       ──► Real-Time Telemetry & Stream Manager        │
│  • WSS /stream/{uuid}   ──► Asynchronous Kernel-Tuned Socket Relay      │
│  • GET /manifest        ──► Unified Multi-Client Distribution Feed      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Direct TCP Stream (TCP_NODELAY)
                                     ▼
                        ┌────────────────────────┐
                        │ Edge Socket Destination│
                        └────────────────────────┘
```

---

## ✨ Key Features

- **Optimized for Seenode:** Zero-config container builds; works seamlessly with Seenode's dynamic `$PORT` injection and SSL edge termination.
- **Kernel-Level Socket Tuning:** Implements `TCP_NODELAY`, `TCP_QUICKACK`, `SO_SNDBUF` (512KB), and a 20-second `TCP_USER_TIMEOUT` to maintain rock-solid connectivity under volatile mobile networks.
- **Adaptive Flow Gate:** Employs Exponentially Weighted Moving Average (EWMA) quota accounting, avoiding lock contention and CPU bottlenecks during sustained high-throughput streams.
- **Embedded Administrative Console:** Modern red-dark interface featuring real-time connection counters, traffic gauges, one-click link exports, and QR code generation.
- **Atomic Persistence Engine:** State is saved atomically to disk (`midoxy_state.json`) with debounced I/O writes, ensuring zero data loss across container restarts. Optional remote Redis backend is also supported.
- **Host Agnostic:** Dynamically extracts the active host from `X-Forwarded-Host` and `Host` request headers, automatically generating correct connection URLs regardless of the domain or CDN layer.

---

## 🚀 Seenode Cloud Deployment Guide

Deploying Midoxy to **Seenode** takes under two minutes directly from your Git repository:

### Step 1: Create a Repository
1. Push this project to your GitHub account (recommended as a **Private** repository).

### Step 2: Create a New App on Seenode
1. Log in to your [Seenode Console](https://seenode.com).
2. Click **Create New App** (or **Deploy from Git**).
3. Connect your GitHub account and select the **Midoxy** repository.
4. Select the **main** branch.

### Step 3: Configure Build & Runtime
Seenode automatically detects the Python runtime from `requirements.txt`:
- **Runtime:** `Python 3.11+`
- **Build Command:** *(Leave default or `pip install -r requirements.txt`)*
- **Start Command:**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
  ```
  *(A `Procfile` is included in the root directory for automated detection).*

### Step 4: Configure Environment Variables
In your Seenode app settings under **Environment Variables**, add the following:

| Key | Recommended Value | Purpose |
| :--- | :--- | :--- |
| `ADMIN_PASSWORD` | `ChooseAStrongPassword` | Password to access `/login` and `/dashboard` |
| `DATA_DIR` | `data` | Directory for persistent state storage |
| `WS_PATH_PREFIX` | `/stream` | Path prefix for active socket tunnels |

### Step 5: Deploy & Verify
1. Click **Deploy**.
2. Once the build completes and status changes to **Running**, open your Seenode application URL:
   - `https://<your-app>.seenode.app/` displays the professional portfolio front page.
   - `https://<your-app>.seenode.app/health` returns `{"status": "ok"}`.
   - `https://<your-app>.seenode.app/login` provides access to your administrative control panel.

---

## 💻 Local Development

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup Instructions

```bash
# 1. Clone repository
git clone https://github.com/TheMido/Midoxy.git
cd Midoxy

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch local development server
python main.py
```

The application will start on `http://127.0.0.1:8000`.

---

## ⚙️ Environment Configuration

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `PORT` | Integer | `8000` | Port on which Uvicorn binds (auto-set by Seenode). |
| `ADMIN_PASSWORD` | String | `123456` | Master password for console login. |
| `DATA_DIR` | String | `data` | Path to persistent storage directory. |
| `PUBLIC_DOMAIN` | String | *(Auto)* | Override domain for connection strings if behind a custom CDN. |
| `REDIS_URL` | String | *(None)* | Optional Redis connection string for external state storage. |
| `WS_PATH_PREFIX` | String | `/stream` | Configurable base path for client connections. |
| `SUB_PATH_PREFIX`| String | `/feed` | Configurable base path for single-client subscription feeds. |

---

## 🩺 Health & Observability

Midoxy includes a lightweight health probe compatible with Seenode's zero-downtime health checkers:

```http
GET /health HTTP/1.1
Host: your-app.seenode.app
```

**Response:**
```json
{
  "status": "ok",
  "uptime": "2d 4h",
  "active": 3
}
```

---

## 📄 License & Maintainer

Distributed under the **MIT License**. See [`LICENSE`](./LICENSE) for full details.

- **Author / Maintainer:** [@OFFL1NE](https://t.me/OFFL1NE)
- **Repository:** [TheMido/Midoxy](https://github.com/TheMido/Midoxy)
