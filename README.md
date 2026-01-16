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
  <a href="#-10-layer-architecture">Architecture</a> •
  <a href="#-unique-features">Unique Features</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-license">License</a>
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
- **📊 Training Data** - Logs all interactions for fine-tuning your own models
- **🏠 Local-First** - Optimized for Ollama and local LLMs

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **10-Layer Architecture** | Specialized agents for each phase of development |
| **Circuit Breaker** | Prevents cascade failures with automatic recovery |
| **Docker Sandbox** | Execute code safely in isolated containers |
| **Stacked Diffs** | Advanced Git workflow for complex changes |
| **Vision Analysis** | Analyze images and screenshots with VLMs |
| **SEO-First Development** | Research competitors before building |
| **LLM Tracer** | Log all interactions for fine-tuning |
| **ChromaDB Memory** | Semantic search over past solutions |

---

## 📦 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/David2024patton/iTaK-Agent-Framework.git
cd iTaK-Agent-Framework

# Install in development mode
pip install -e .
```

### Basic Usage

```python
from itak import Agent, Crew, Task

# Create agents
analyst = Agent(
    role="Senior Requirements Analyst",
    goal="Parse user intent and gather requirements",
    backstory="You are an expert at understanding complex requests."
)

builder = Agent(
    role="Senior Software Engineer", 
    goal="Write clean, maintainable code",
    backstory="You follow best practices and design patterns."
)

# Define tasks
analysis_task = Task(
    description="Analyze the requirements for building a REST API",
    agent=analyst,
    expected_output="A detailed list of requirements"
)

build_task = Task(
    description="Implement the REST API based on requirements",
    agent=builder,
    expected_output="Working Python code for the API"
)

# Create and run the crew
crew = Crew(
    agents=[analyst, builder],
    tasks=[analysis_task, build_task]
)

result = crew.kickoff()
print(result)
```

### Using Layer Presets

```python
from itak.layers import get_layer_preset, create_agent_from_preset

# Get predefined agent configurations
analyst_preset = get_layer_preset("analyst")
builder_preset = get_layer_preset("builder")
validator_preset = get_layer_preset("validator")

# Create agents from presets
analyst = create_agent_from_preset(analyst_preset)
builder = create_agent_from_preset(builder_preset)
```

---

## 🏗️ 10-Layer Architecture

iTaK uses a **specialized 10-layer architecture** where each layer has a specific role:

| Layer | Name | Role | Tools |
|:-----:|------|------|-------|
| 1 | **Analyst** | Parse intent, gather requirements | `search_memory`, `ask_user` |
| 2 | **Recon** | Research, web scraping, data gathering | `web_research`, `web_scraper` |
| 3 | **Orchestrator** | Plan and delegate work | `create_task`, `delegate` |
| 4 | **Builder** | Write code and content | `write_code`, `edit_file` |
| 5 | **Validator** | Test, lint, verify quality | `run_tests`, `lint_code` |
| 6 | **Sandbox** | Execute code safely in Docker | `run_safe`, `docker_exec` |
| 7 | **Deployer** | Deploy to production | `docker_deploy`, `ssh_client` |
| 8 | **Librarian** | Manage memory and skills | `add_memory`, `register_skill` |
| 9 | **Healer** | Monitor, detect failures, auto-recover | `health_check`, `circuit_breaker` |
| 10 | **Swarm** | Multi-agent collaboration | `spawn_agent`, `parallel_exec` |

---

## 🔥 Unique Features

### Circuit Breaker (Self-Healing)

```python
from itak.utilities.circuit_breaker import circuit_protected, get_all_circuits

@circuit_protected("ollama_api", failure_threshold=3, recovery_timeout=30)
def call_ollama(prompt):
    # If this fails 3 times, circuit opens and requests are rejected
    # After 30 seconds, it tries again (half-open state)
    return ollama.generate(prompt)

# Check circuit status
print(get_all_circuits())
```

### Docker Sandbox

```python
from itak.security.sandbox import run_in_sandbox

# Execute untrusted code safely
result = run_in_sandbox("""
import os
print('Running in isolated container!')
print('Cannot access host filesystem')
""")

print(result.stdout)  # Output from container
print(result.success)  # True if execution succeeded
```

### LLM Tracer (Training Data)

```python
from itak.telemetry.llm_tracer import get_tracer

tracer = get_tracer()

# Log an interaction
tracer.log(
    model="qwen3:4b",
    prompt="Write a hello world in Python",
    response="print('Hello, World!')",
    tokens_in=10,
    tokens_out=5
)

# Export for fine-tuning
tracer.export("training_data.jsonl", format="sharegpt")
```

### SEO-First Development

```python
from tools.seo_analyzer import research_competitors, generate_seo_brief

# Research before building
analysis = research_competitors("python web framework tutorial")

print(f"Common keywords: {analysis.common_keywords}")
print(f"Recommendations: {analysis.recommendations}")

# Generate content brief
brief = generate_seo_brief("FastAPI REST API tutorial")
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# LLM Configuration
OLLAMA_URL=http://127.0.0.1:11434
LLM_BASE_URL=http://127.0.0.1:11434/v1
VISION_MODEL=llava

# Services
SEARXNG_URL=http://localhost:29541
CHROMADB_URL=http://localhost:29800

# Tracing
TRACE_ENABLED=true
ITAK_TRACE_DIR=logs/traces

# Sandbox
ITAK_SNAPSHOT_DIR=data/snapshots
```

### Using with Ollama

```python
from itak import LLM

# Configure Ollama as the LLM provider
llm = LLM(
    model="ollama/qwen3:4b",
    base_url="http://localhost:11434"
)

# Use with an agent
agent = Agent(
    role="Developer",
    goal="Write Python code",
    llm=llm
)
```

---

## 📁 Project Structure

```
iTaK-Agent-Framework/
├── src/itak/                    # Core framework
│   ├── layers/                  # 10-layer architecture
│   │   └── presets.py           # Layer agent presets
│   ├── utilities/
│   │   └── circuit_breaker.py   # Self-healing pattern
│   ├── security/
│   │   └── sandbox.py           # Docker sandbox
│   ├── telemetry/
│   │   └── llm_tracer.py        # Training data collection
│   ├── agents/                  # Agent implementations
│   ├── memory/                  # Memory systems
│   ├── flow/                    # Event-driven flows
│   └── cli/                     # Command line interface
├── tools/                       # Tool library
│   ├── stacked_diffs.py         # Git workflow
│   ├── vision_analysis.py       # Image analysis
│   └── seo_analyzer.py          # SEO tools
├── licenses/
│   └── CREWAI_MIT_LICENSE       # Original CrewAI license
├── pyproject.toml
└── README.md
```

---

## 🎯 Operating Principles

iTaK follows 14 operating principles for autonomous operation:

1. **Ingestion Before Invention** - Research before building
2. **Skills Over Scripts** - Reuse verified solutions
3. **Monitoring is Testing** - Log everything
4. **Progressive Trust** - Sandbox first, production later
5. **Deployment-First** - Think about deployment from the start
6. **Hot Reload** - Test changes in isolation
7. **Rate Limiting** - Circuit breaker pattern
8. **Model Routing** - Right model for each task
9. **Inference Guardrails** - Token limits, temperature control
10. **Visual Verification** - Screenshot UI changes
11. **Autonomous Completion** - Loop until done
12. **Content Population** - No empty placeholders
13. **SEO-First** - Research competitors before building
14. **Repair First** - Fix issues before reporting

---

## 🤝 Acknowledgments

iTaK Agent Framework is built upon [CrewAI](https://github.com/crewAIInc/crewAI), licensed under the MIT License. We thank the CrewAI team for their foundational work in multi-agent orchestration.

---

## 📜 License

MIT License - see [LICENSE](licenses/CREWAI_MIT_LICENSE) for details.

---

<p align="center">
  <strong>Built for builders. Powered by local AI.</strong><br>
  Created by <a href="https://github.com/David2024patton">David Patton</a>
</p>
