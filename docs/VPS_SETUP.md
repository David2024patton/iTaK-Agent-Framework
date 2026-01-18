# VPS Remote Access Setup Guide

This guide explains how to connect your **local iTaK services** to a **VPS (Virtual Private Server)** so you can access your AI tools from anywhere in the world - even without a static IP address.

## Why Do I Need This?

Most home internet connections have **dynamic IP addresses** that change regularly. This makes it impossible to access your local services from the outside. We solve this using **FRP (Fast Reverse Proxy)** - a secure tunnel between your local machine and your VPS.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           YOUR VPS (Your IP)                            │
│                                                                         │
│  ┌──────────────┐    ┌──────────────────────────────────────────────┐  │
│  │  FRP Server  │    │          Open Ports (Internet)               │  │
│  │   (frps)     │    │  • 7000  - FRP Control (Client Connection)   │  │
│  │  Port: 7000  │    │  • 28934 - API Gateway                       │  │
│  └──────────────┘    │  • 11434 - Ollama LLM                        │  │
│                      │  • 39281 - Playwright Browser                │  │
│                      └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │ SECURE TUNNEL (TCP)
                                    │
┌─────────────────────────────────────────────────────────────────────────┐
│                        YOUR LOCAL PC                                    │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ FRP Client   │  │ FastAPI      │  │ Playwright   │  │ SearXNG     │ │
│  │   (frpc)     │  │ Gateway      │  │ Server       │  │             │ │
│  │              │  │ Port: 28934  │  │ Port: 39281  │  │ Port: 48192 │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └─────────────┘ │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐                                    │
│  │ Ollama LLM   │  │ ChromaDB     │                                    │
│  │ Port: 11434  │  │ Port: 8000   │                                    │
│  └──────────────┘  └──────────────┘                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Alternative: Cloudflare Tunnel

If you don't have a VPS, you can use **Cloudflare Tunnel** for free:

- **Temporary Tunnel**: Quick public URL, no account needed
- **Permanent Tunnel**: Custom domain, requires free Cloudflare account

Both options are available in iTaK via the `/api` command or menu option `[7] API Gateway`.

---

## Part 1: VPS Setup (One-Time)

### Prerequisites

- A VPS with Docker installed ($5/month from DigitalOcean, Vultr, Linode, etc.)
- SSH access to your VPS
- Root or sudo privileges

### Step 1: Open Firewall Ports

> [!IMPORTANT]
> You MUST open these ports on your VPS firewall BEFORE proceeding.

| Port  | Purpose                          |
|-------|----------------------------------|
| 7000  | FRP Control (Client Connection)  |
| 28934 | API Gateway                      |
| 11434 | Ollama LLM Access                |
| 39281 | Playwright WebSocket             |

**For Ubuntu/Debian (UFW):**
```bash
sudo ufw allow 7000/tcp
sudo ufw allow 28934/tcp
sudo ufw allow 11434/tcp
sudo ufw allow 39281/tcp
sudo ufw reload
```

**For cloud providers (AWS, GCP, Azure, DigitalOcean):**
Also configure your Security Group / Firewall to allow these inbound ports.

### Step 2: Create FRP Server Directory

```bash
ssh root@YOUR_VPS_IP
mkdir -p /root/frp-server
cd /root/frp-server
```

### Step 3: Generate Auth Token

```bash
# Generate a secure random token
openssl rand -hex 16
```

Save this token - you'll need it for both server and client configuration.

### Step 4: Create Configuration Files

#### File: `frps.toml`

```bash
cat > frps.toml << 'EOF'
# FRP Server Configuration
bindPort = 7000
auth.method = "token"
auth.token = "YOUR_TOKEN_HERE"
EOF
```

> Replace `YOUR_TOKEN_HERE` with your generated token.

#### File: `docker-compose.yml`

```bash
cat > docker-compose.yml << 'EOF'
services:
  frps:
    image: snowdreamtech/frps
    container_name: frps
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./frps.toml:/etc/frp/frps.toml
EOF
```

### Step 5: Start FRP Server

```bash
docker compose up -d
docker logs frps
```

**Expected Output:**
```
[I] frps started successfully
```

---

## Part 2: Local Setup (Automatic)

When you run iTaK, the local setup is **automatic**. The `npm install` process:

1. ✅ Installs Docker Desktop (if needed)
2. ✅ Starts Ollama, ChromaDB, Playwright, SearXNG containers
3. ✅ Generates `.env` file with service URLs

### Configure VPS Connection

Use the `/api` command in iTaK to configure your VPS connection:

```
itak
> /api
```

Then select **[5] Configure VPS Connection** and enter:
- Your VPS IP address
- Your FRP auth token

This creates the FRP client configuration and connects your local services to your VPS.

---

## Part 3: Testing the Connection

### From Your VPS (or anywhere)

**Test API Gateway:**
```bash
curl http://YOUR_VPS_IP:28934/health
```

**Test Ollama:**
```bash
curl http://YOUR_VPS_IP:11434
# Should return: "Ollama is running"
```

---

## Port Reference

| Service          | Local Port | VPS Port | Protocol |
|------------------|------------|----------|----------|
| API Gateway      | 28934      | 28934    | HTTP     |
| Ollama LLM       | 11434      | 11434    | HTTP     |
| Playwright       | 39281      | 39281    | WebSocket|
| SearXNG          | 48192      | N/A      | HTTP     |
| ChromaDB         | 8000       | N/A      | HTTP     |
| FRP Control      | N/A        | 7000     | TCP      |

---

## Troubleshooting

### FRP Client Can't Connect

1. **Check VPS firewall:** Ensure port 7000 is open
2. **Check token:** Must match exactly between server and client
3. **Check VPS logs:** `docker logs frps`

### Services Not Accessible

1. **Check local services:** `docker ps`
2. **Check FRP client logs:** `docker logs frpc`
3. **Verify tunnel status:** Use `/api` → `[4] Show Service Status`

---

## Security Notes

> [!CAUTION]
> - Use a strong, unique token for FRP authentication
> - Consider IP whitelisting on your VPS firewall
> - Never commit tokens to public repositories
> - The tunneled ports are publicly accessible - secure your services accordingly
