# iTaK Framework - First-Time Setup

## Quick Start

After installing iTaK, run the bootstrap script to auto-deploy all necessary services:

```bash
# Install iTaK in development mode
pip install -e .

# Run first-time setup (auto-deploys Docker containers)
python -m itak.setup
```

## What the Bootstrap Does

The bootstrap script automatically:

1. **Scans Your System**
   - Detects WSL vs Windows
   - Checks for NVIDIA GPU
   - Measures CPU cores and RAM
   - Scans storage drives

2. **Auto-Deploys Docker Containers**
   - **Ollama** (port 11434) - LLM backend
   - **ChromaDB** (port 29800) - Vector database for memory
   - Automatically detects and reuses existing containers

3. **Configures Telemetry**
   - Points iTaK telemetry to VPS (145.79.2.67:4318)
   - All traces sent to your private Grafana instance

4. **Generates System Profile**
   - Saves hardware specs to `users/docs/system_profile.json`
   - Used for optimal model routing

## Manual Setup (if needed)

If you need to deploy services manually:

```bash
# Ollama
docker run -d --gpus=all -p 11434:11434 --name ollama --restart unless-stopped ollama/ollama

# ChromaDB
docker run -d -p 29800:8000 --name shared-chromadb --restart unless-stopped chromadb/chroma
```

## Verify Installation

Run the health check:

```bash
python start.py
```

This will verify all services are running and telemetry is configured correctly.

## View Telemetry

All iTaK agent traces are sent to:
- **Grafana UI**: http://145.79.2.67:3456/ (admin / itak2026)
- **Raw JSONL**: `/opt/itak-telemetry/telemetry-data/traces.jsonl` on VPS

## Troubleshooting

**Docker not running:**
```bash
# Windows
net start com.docker.service

# WSL
sudo service docker start
```

**Containers not starting:**
```bash
# Check Docker logs
docker logs ollama
docker logs shared-chromadb

# Restart containers
docker restart ollama shared-chromadb
```

**Telemetry not working:**
- Check VPS is accessible: `ping 145.79.2.67`
- Verify port 4318 is open
- Run connection test: `python test_telemetry_connection.py`
