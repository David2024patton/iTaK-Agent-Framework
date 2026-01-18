<p align="center">
  <img src="https://img.shields.io/badge/iTaK-Agent_Framework-blue?style=for-the-badge&logo=robot" alt="iTaK Agent Framework">
</p>

<h1 align="center">iTaK Agent Framework</h1>

<p align="center">
  <strong>Intelligent Task Automation Kernel</strong><br>
  A powerful multi-agent automation framework with self-healing capabilities and 10-layer architecture.
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-remote-access">Remote Access</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-model-catalog">Models</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/Ollama-Supported-orange?logo=ollama" alt="Ollama Ready">
</p>

---

## 🚀 What is iTaK?

iTaK (Intelligent Task Automation Kernel) is a **production-ready multi-agent framework** that turns any AI into an autonomous coding assistant with:

- **🔧 Self-Healing** - Automatically detects and recovers from failures
- **🧠 Persistent Memory** - Remembers past solutions via ChromaDB
- **🐳 Safe Execution** - Runs untrusted code in Docker sandboxes
- **🌐 Remote Access** - Access your local AI from anywhere via VPS or Cloudflare tunnels
- **🏠 Local-First** - Optimized for Ollama and local LLMs

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **One-Command Setup** | `npm install` auto-configures Docker, Ollama, and all services |
| **10-Layer Architecture** | Specialized agents for each phase of development |
| **Remote Access** | Access local AI from anywhere via [VPS tunnels](docs/VPS_SETUP.md) or Cloudflare |
| **API Gateway** | FastAPI gateway with Playwright, SearXNG, and ChromaDB |
| **Circuit Breaker** | Prevents cascade failures with automatic recovery |
| **Docker Sandbox** | Execute code safely in isolated containers |
| **LLM Tracer** | Log all interactions for fine-tuning |

---

## 📦 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/David2024patton/iTaK-Agent-Framework.git
cd iTaK-Agent-Framework

# One command does everything
npm install
```

**`npm install` automatically:**
- ✅ Detects your OS (Windows/Mac/Linux)
- ✅ Installs Docker Desktop and Ollama (if needed)
- ✅ Starts all containers (Ollama, ChromaDB, Playwright, SearXNG)
- ✅ Pulls the default LLM model (`qwen3-vl:2b`)
- ✅ Generates `.env` with service URLs
- ✅ Launches `itak` CLI

### Using iTaK

After install, just run:

```bash
itak
```

**Main Menu:**
```
[1] 🌐 Web App      - HTML/CSS/JS web application
[2] 🐍 Python       - Python script or automation
[3] ⚡ API/Backend  - REST API or backend service
[4] 🤖 AI Agent     - AI agent or workflow
[5] 📝 Custom       - Describe your project freely
[6] 💬 Chat         - Interactive coding assistance

[7] ⚡ API Gateway  - Manage tunnels and remote access
```

---

## 🌐 Remote Access

Access your local AI services from anywhere - even without a static IP.

### Option 1: Cloudflare Tunnel (Easiest)

No VPS or account needed! From iTaK:

```bash
itak
> /api
# Select [2] Cloudflare Tunnel (Quick)
```

Gets you a public URL like `https://random-name.trycloudflare.com`

### Option 2: VPS + FRP Tunnel (Best for Production)

For permanent remote access with your own domain:

1. **Set up VPS** → [docs/VPS_SETUP.md](docs/VPS_SETUP.md)
2. **Configure in iTaK:**
   ```bash
   itak
   > /api
   # Select [4] Configure VPS Connection
   ```
3. **Start tunnel:**
   ```bash
   # Select [5] Start/Stop FRP Tunnel
   ```

Your local services are now accessible at `http://YOUR_VPS_IP:PORT`

---

## 🏗️ Architecture

iTaK uses a **10-layer architecture** where each layer has a specific role:

| Layer | Name | Role |
|:-----:|------|------|
| 1 | **Analyst** | Parse intent, gather requirements |
| 2 | **Recon** | Research, web scraping, data gathering |
| 3 | **Orchestrator** | Plan and delegate work |
| 4 | **Builder** | Write code and content |
| 5 | **Validator** | Test, lint, verify quality |
| 6 | **Sandbox** | Execute code safely in Docker |
| 7 | **Deployer** | Deploy to production |
| 8 | **Librarian** | Manage memory and skills |
| 9 | **Healer** | Monitor, detect failures, auto-recover |
| 10 | **Swarm** | Multi-agent collaboration |

---

## 📁 Project Structure

```
iTaK-Agent-Framework/
├── src/itak/              # Core framework
│   ├── cli/               # Command line interface
│   │   └── api_manager.py # API Gateway manager
│   ├── layers/            # 10-layer architecture
│   ├── utilities/         # Circuit breaker, helpers
│   └── security/          # Docker sandbox
├── docker/
│   └── api-gateway/       # Docker compose for all services
├── docs/
│   └── VPS_SETUP.md       # Remote access setup guide
├── scripts/
│   └── postinstall.js     # Auto-setup script
└── README.md
```

---

## 🐳 Docker Services

After `npm install`, these containers run under the `api-gateway` project:

| Service | Port | Description |
|---------|------|-------------|
| **Ollama** | 11434 | Local LLM server |
| **ChromaDB** | 29800 | Vector memory database |
| **Playwright** | 39281 | Browser automation |
| **SearXNG** | 48192 | Private search engine |

---

## 🤖 Model Catalog

iTaK includes a curated catalog of **100+ models** across 20 domain categories. Run `itak` and select a project type to get matched with the best model for your task.

**Popular Models:**
- `qwen3-vl:2b` - Default, fast vision + text
- `qwen2.5-coder:7b` - Specialized for coding
- `deepseek-r1:8b` - Deep reasoning

---

## 🤝 Acknowledgments

Built upon [CrewAI](https://github.com/crewAIInc/crewAI) (MIT License).

---

## 📄 License

MIT License - see [LICENSE](licenses/LICENSE)
