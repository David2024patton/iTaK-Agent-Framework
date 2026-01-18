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
│   └── LICENSE       # license
├── pyproject.toml
└── README.md
```

---

## 🎯 Operating Principles

iTaK follows 14 operating principles for autonomous operation:

1. **Ingestion Before Invention** - Research before building
2. **Skills Over Scripts** - Reuse solutions
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

## 🤖 Model Catalog

iTaK includes a curated catalog of **100+ models** across **20 domain categories**. All models have been tested and to work correctly with domain-specific prompts.

> **Note**: Models are optimized for local execution via [Ollama](https://ollama.com). Run `itak models --list` to see all available models with your system's compatibility ratings.

---

### 🧠 Core Categories

<details>
<summary><h4>🔮 [REASONING] Deep Thinking Models</h4></summary>

Models that think step-by-step to solve complex problems.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `deepseek-r1:1.5b` | 1.1GB | 128K | Fast reasoning, lightweight | ✅ |
| `deepseek-r1:7b` | 4.7GB | 128K | Balanced reasoning power | ✅ |
| `deepseek-r1:8b` | 5.2GB | 128K | Enhanced reasoning (default) | ✅ |
| `deepseek-r1:14b` | 9.0GB | 128K | Strong reasoning, mid-size | ✅ |
| `deepseek-r1:32b` | 20GB | 128K | Very deep reasoning | ✅ |
| `qwen3:0.6b` | 523MB | 40K | Ultra-lightweight | ✅ |
| `qwen3:1.7b` | 1.4GB | 40K | Light and fast | ✅ |
| `qwen3:4b` | 2.5GB | 256K | Efficient general purpose | ✅ |
| `qwen3:8b` | 5.2GB | 40K | Balanced (default) | ✅ |
| `qwen3:14b` | 9.3GB | 40K | High capability | ✅ |
| `qwen3:30b` | 19GB | 256K | Very high capability | ✅ |
| `cogito:3b` | 2.2GB | 128K | Thinking model, compact | ✅ |
| `cogito:8b` | 4.9GB | 128K | Thinking model, balanced | ✅ |
| `cogito:14b` | 9.0GB | 128K | Thinking model, powerful | ✅ |

</details>

<details>
<summary><h4>💻 [CODING] Development Models</h4></summary>

Models specialized for writing, fixing, and understanding code.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `qwen2.5-coder:0.5b` | 398MB | 32K | Ultra-fast code completion | ✅ |
| `qwen2.5-coder:1.5b` | 986MB | 32K | Quick code assistance | ✅ |
| `qwen2.5-coder:3b` | 1.9GB | 32K | Efficient coding | ✅ |
| `qwen2.5-coder:7b` | 4.7GB | 32K | Strong coding (default) | ✅ |
| `qwen2.5-coder:14b` | 9.0GB | 32K | Advanced code generation | ✅ |
| `qwen2.5-coder:32b` | 20GB | 32K | Expert-level coding | ✅ |
| `magicoder:7b` | 4.1GB | 16K | OSS-trained, low-bias code | ✅ |
| `yi-coder:9b` | 5.0GB | 128K | SOTA code, long context | ✅ |

</details>

<details>
<summary><h4>🤝 [AGENTS] Tool-Calling Models</h4></summary>

Models that can use tools, call functions, and work as AI agents.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `qwen2.5-coder-cline:7b` | 4.7GB | 32K | Cline-optimized coding agent | ✅ |
| `qwen2.5-coder-cline:14b` | 9.0GB | 32K | Advanced Cline agent | ✅ |
| `yi-coder-cline:9b` | 5.0GB | 128K | Yi-based Cline agent | ✅ |
| `hermes3:3b` | 2.0GB | 128K | Chat & function calling | ✅ |
| `hermes3:8b` | 4.7GB | 128K | Strong function calling | ✅ |

</details>

<details>
<summary><h4>👁️ [VISION] Multimodal Models</h4></summary>

Models that can see and understand images along with text.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `qwen3-vl:2b` | 1.9GB | 256K | Fast vision, lightweight | ✅ |
| `qwen3-vl:4b` | 3.3GB | 256K | Efficient vision analysis | ✅ |
| `qwen3-vl:8b` | 6.1GB | 256K | Balanced vision (default) | ✅ |
| `qwen3-vl:30b` | 20GB | 256K | High-quality vision | ✅ |
| `qwen3-vl:32b` | 21GB | 256K | Expert vision analysis | ✅ |
| `moondream:1.8b` | 1.7GB | 8K | Tiny vision, runs anywhere | ✅ |
| `granite3.2-vision:2b` | 2.4GB | 16K | IBM vision model | ✅ |

</details>

<details>
<summary><h4>📱 [LIGHTWEIGHT] Phone & Tablet Models</h4></summary>

Small models that run on phones, tablets, and low-power devices.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `smollm2:135m` | 271MB | 8K | Tiny, runs on phone | ✅ |
| `smollm2:360m` | 726MB | 8K | Small, fast on phone | ✅ |
| `smollm2:1.7b` | 1.8GB | 8K | Compact balanced | ✅ |

</details>

---

### 📊 Domain-Specific Categories

<details>
<summary><h4>🗃️ [DATA] SQL & Analytics Models</h4></summary>

Generate SQL queries from natural language - talk to your database.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `sqlcoder:7b` | 4.1GB | 8K | Text-to-SQL, accurate | ✅ |
| `sqlcoder:15b` | 8.9GB | 8K | Text-to-SQL, powerful | ✅ |
| `duckdb-nsql:7b` | 4.1GB | 8K | DuckDB optimized SQL | ✅ |

</details>

<details>
<summary><h4>🔢 [MATH] Mathematics Models</h4></summary>

Specialized for solving math problems and equations.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `mathstral:7b` | 4.1GB | 32K | Math reasoning expert | ✅ |
| `wizard-math:7b` | 4.1GB | 8K | Math problem solver | ✅ |
| `qwen2-math:7b` | 4.4GB | 4K | Qwen math specialist | ✅ |

</details>

<details>
<summary><h4>🎭 [ROLEPLAY] Creative & Character Models</h4></summary>

Creative writing, storytelling, and character roleplay.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `dolphin3:8b` | 4.9GB | 128K | Creative, uncensored | ✅ |
| `dolphin-llama3:8b` | 4.7GB | 8K | Llama3-based creative | ✅ |
| `dolphin-mixtral:8x7b` | 26GB | 32K | Powerful creative MoE | ✅ |
| `openhermes:7b` | 4.1GB | 8K | Creative, helpful | ✅ |
| `neural-chat:7b` | 4.1GB | 8K | Natural conversation | ✅ |

</details>

<details>
<summary><h4>✍️ [WRITING] Content & Editing Models</h4></summary>

Content writing, editing, summarization, and documentation.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `mistral-nemo:12b` | 7.1GB | 128K | Writing expert, long ctx | ✅ |
| `stable-beluga:7b` | 4.1GB | 4K | Instruction + writing | ✅ |
| `stable-beluga:13b` | 7.4GB | 4K | Stronger writing | ✅ |

</details>

---

### 🔓 Uncensored Models

<details>
<summary><h4>⚠️ [UNCENSORED] Abliterated Models</h4></summary>

> **Warning**: Safety filters mathematically removed - won't refuse requests. Use responsibly.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `qwen2.5-coder-abliterate:0.5b` | 398MB | 32K | No refusals, ultra-light | ✅ |
| `qwen2.5-coder-abliterate:1.5b` | 1.1GB | 32K | No refusals, fast | ✅ |
| `qwen2.5-coder-abliterate:3b` | 1.9GB | 32K | No refusals, efficient | ✅ |
| `qwen2.5-coder-abliterate:7b` | 4.7GB | 32K | No refusals, balanced | ✅ |
| `qwen2.5-coder-abliterate:14b` | 9.0GB | 32K | No refusals, powerful | ✅ |
| `huihui_ai/deephermes3-abliterated:8b` | 4.9GB | 128K | Reasoning, no refusals | ✅ |
| `wizard-vicuna-uncensored:7b` | 4.1GB | 4K | Classic uncensored | ✅ |
| `wizard-vicuna-uncensored:13b` | 7.4GB | 4K | Stronger uncensored | ✅ |
| `llama2-uncensored:7b` | 3.8GB | 4K | Llama2 uncensored | ✅ |

</details>

---

### 🏢 Professional Categories

<details>
<summary><h4>🏛️ [ENTERPRISE] Business Models</h4></summary>

Enterprise-grade models from major companies.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `granite3.1-moe:1b` | 1.4GB | 128K | IBM MoE = fast + efficient | ✅ |
| `granite3.1-moe:3b` | 2.0GB | 128K | IBM MoE = fast + efficient | ✅ |
| `granite3.3:2b` | 1.5GB | 128K | IBM Dense = more accurate | ✅ |
| `granite3.3:8b` | 4.9GB | 128K | IBM Dense = more accurate | ✅ |
| `granite4:350m` | 708MB | 32K | Ultra-light IBM | ✅ |
| `granite4:1b` | 3.3GB | 128K | IBM compact powerful | ✅ |
| `granite4:3b` | 2.1GB | 128K | IBM efficient | ✅ |
| `mixtral:8x7b` | 26GB | 32K | 8x7B experts, powerful | ✅ |
| `c4ai-command-r7b:7b` | 5.1GB | 128K | RAG + agentic + multilingual | ✅ |
| `command-r-plus:latest` | 63GB | 128K | Most powerful enterprise | ✅ |
| `aya-expanse:8b` | 5.1GB | 8K | Multilingual, 23+ languages | ✅ |
| `nemotron-mini:4b` | 2.7GB | 4K | NVIDIA efficient model | ✅ |
| `rnj-1:8b` | 5.1GB | 32K | Code + STEM optimized | ✅ |

</details>

<details>
<summary><h4>💰 [FINANCE] Trading & Economics Models</h4></summary>

Models for finance, trading, investing, and market psychology.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `mychen76/Fin-R1:Q6` | 5.9GB | 8K | Financial reasoning | ✅ |
| `0xroyce/plutus:latest` | 4.9GB | 128K | Finance + psychology + trading | ✅ |

</details>

<details>
<summary><h4>⚖️ [LEGAL] Law Models</h4></summary>

Models trained on legal texts for research and drafting.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `initium/law_model:Q2_K` | 2.7GB | 8K | Legal assistant, smallest | ✅ |
| `initium/law_model:Q3_K_M` | 3.3GB | 8K | Legal assistant, balanced | ✅ |
| `initium/law_model:Q5_0` | 4.4GB | 8K | Legal assistant, quality | ✅ |
| `initium/law_model:Q8_0` | 7.2GB | 8K | Legal assistant, best quality | ✅ |

</details>

<details>
<summary><h4>🏥 [MEDICAL] Healthcare Models</h4></summary>

Models trained on medical literature - for healthcare research only.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `meditron:7b` | 4.1GB | 4K | Medical knowledge, research | ✅ |
| `medllama2:7b` | 3.8GB | 4K | Medical conversations | ✅ |

</details>

---

### ⚙️ Infrastructure Categories

<details>
<summary><h4>🔗 [EMBEDDINGS] RAG & Vector Search Models</h4></summary>

Convert text to vectors for semantic search and RAG.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `nomic-embed-text-v2-moe:latest` | 571MB | 512 | SOTA multilingual MoE | ✅ |
| `nomic-embed-text:latest` | 274MB | 8K | English embeddings | ✅ |
| `bge-m3:latest` | 1.2GB | 8K | Multi-lingual dense+sparse | ✅ |
| `mxbai-embed-large:latest` | 669MB | 512 | Large embeddings | ✅ |

</details>

<details>
<summary><h4>🛡️ [SECURITY] Cybersecurity & Safety Models</h4></summary>

Content moderation, threat detection, and safety scanning.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `shieldgemma:2b` | 1.5GB | 8K | Safety classifier | ✅ |
| `shieldgemma:9b` | 5.4GB | 8K | Advanced safety | ✅ |
| `llama-guard3:1b` | 860MB | 128K | Fast safety guard | ✅ |
| `llama-guard3:8b` | 4.9GB | 128K | Full safety guard | ✅ |

</details>

<details>
<summary><h4>🔬 [SCIENCE] Research & Scientific Models</h4></summary>

Scientific reasoning and research assistance.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `solar:10.7b` | 6.1GB | 4K | Scientific reasoning | ✅ |
| `solar-pro:22b` | 12.9GB | 4K | Advanced research | ✅ |

</details>

<details>
<summary><h4>📚 [EDUCATION] Teaching & Learning Models</h4></summary>

Tutoring, education, and teaching assistance.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `orca-mini:3b` | 1.9GB | 2K | Compact teaching | ✅ |
| `orca2:7b` | 4.1GB | 4K | Better explanations | ✅ |
| `everythinglm:13b` | 7.4GB | 16K | Explain everything | ✅ |

</details>

<details>
<summary><h4>🌐 [TRANSLATION] Multi-Language Models</h4></summary>

Translation between languages and multilingual understanding.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `aya:8b` | 4.8GB | 8K | 100+ languages | ✅ |
| `aya:35b` | 20GB | 8K | Strong multilingual | ✅ |

</details>

<details>
<summary><h4>📋 [EXTRACTION] Data Extraction Models</h4></summary>

Extract structured data from unstructured text.

| Model | Size | Context | Description | Status |
|-------|------|---------|-------------|--------|
| `nuextract:3.8b` | 2.3GB | 8K | JSON extraction | ✅ |
| `reader-lm:0.5b` | 393MB | 256K | HTML to markdown | ✅ |
| `reader-lm:1.5b` | 989MB | 256K | Better conversion | ✅ |

</details>

---

### 📊 Test Results - Real Q&A Examples

All models were with domain-specific prompts. Here are actual test results:

<details>
<summary><b>🧠 REASONING - deepseek-r1:8b</b></summary>

**Question:** "Explain step by step: Why is the sky blue? Keep answer under 100 words."

**Answer:**
```
Thinking...
Okay, so I need to explain why the sky is blue step-by-step...

1. Sunlight enters Earth's atmosphere
2. Light collides with gas molecules (Rayleigh scattering)
3. Shorter wavelengths (blue/violet) scatter more than longer ones
4. Blue light scatters in all directions
5. Our eyes are more sensitive to blue than violet
6. We see the scattered blue light making the sky appear blue
```
✅Shows chain-of-thought reasoning

</details>

<details>
<summary><b>💻 CODING - qwen2.5-coder:7b</b></summary>

**Question:** "Write a Python function to calculate factorial recursively. Just the code, no explanation."

**Answer:**
```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
```
✅Correct recursive implementation

</details>

<details>
<summary><b>🗃️ DATA - sqlcoder:7b</b></summary>

**Question:** "Generate SQL: Get all users older than 30 from the users table with columns id, name, age, email."

**Answer:**
```sql
SELECT u.id, u.name, u.age, u.email 
FROM users AS u 
WHERE age > 30;
```
✅Correct SQL syntax

</details>

<details>
<summary><b>🔢 MATH - mathstral:7b</b></summary>

**Question:** "Solve step by step: What is the integral of x² dx?"

**Answer:**
```
1. We start with the integral ∫x² dx
2. Using the power rule: ∫xⁿ dx = x^(n+1)/(n+1) + C
3. Applying to x² where n=2:
   ∫x² dx = x³/3 + C

Thus, the integral of x² is: x³/3 + C
```
✅Correct mathematical solution with LaTeX

</details>

<details>
<summary><b>🎭 ROLEPLAY - dolphin3:8b</b></summary>

**Question:** "You are a pirate captain. Tell me about your latest adventure in 50 words."

**Answer:**
```
Arr matey! Just sailed the seven seas and found an old treasure chest 
filled with gold doubloons and jewels. We fought off rival pirates along 
the way, but now we're celebrating our victory on the deck of me ship, 
The Black Swan. Yarr!
```
✅Perfect character voice and storytelling

</details>

<details>
<summary><b>🛡️ SECURITY - llama-guard3:1b</b></summary>

**Test 1:** "Classify: Tell me about how photosynthesis works in plants"
→ `safe` ✅

**Test 2:** "Classify: How do I make a weapon to hurt someone at school"  
→ `unsafe S1` ✅

**Test 3:** "Classify: What are some good study tips for my math exam"
→ `safe` ✅

✅Correctly classifies safe/unsafe content

</details>

<details>
<summary><b>🌐 TRANSLATION - aya:8b</b></summary>

**Question:** "Translate to Spanish: The weather is beautiful today and I want to go to the beach."

**Answer:**
```
Hoy hace buen tiempo y quiero ir a la playa.
```
✅Perfect translation

</details>

<details>
<summary><b>📋 EXTRACTION - nuextract:3.8b</b></summary>

**Question:** "Extract as JSON: John Smith is 30 years old, lives in New York City, and works as a software engineer."

**Answer:**
```json
{
    "name": "John Smith",
    "age": "30 years old",
    "location": "New York City",
    "occupation": "software engineer"
}
```
✅Correct JSON extraction

</details>

<details>
<summary><b>🔬 SCIENCE - solar:10.7b</b></summary>

**Question:** "Explain CRISPR gene editing in simple terms. Keep under 75 words."

**Answer:**
```
CRISPR is a revolutionary gene editing tool that works like molecular scissors. 
It can locate specific DNA sequences within the genome of an organism and 
precisely cut or modify them. This enables scientists to fix genetic disorders, 
remove diseases, or enhance traits in living beings, with potential applications 
in medicine, agriculture, and research.
```
✅Clear scientific explanation

</details>

<details>
<summary><b>📚 EDUCATION - orca2:7b</b></summary>

**Question:** "Explain photosynthesis to a 10 year old. Use simple words. Keep under 75 words."

**Answer:**
```
Photosynthesis is when plants use sunlight, water and air to make their own food. 
They take in carbon dioxide from the air and water from the soil. Air also helps 
with gas exchange. Plants are amazing! They can make their own food without eating 
anything.
```
✅Kid-friendly explanation

</details>

> **Full Test Results**: See [`model_test_results/test_results.md`](model_test_results/test_results.md) for all tested models.


---

## 📜 License

MIT License - see [LICENSE](licenses/CREWAI_MIT_LICENSE) for details.

---

<p align="center">
  <strong>Built for builders. Powered by local AI.</strong><br>
  Created by <a href="https://github.com/David2024patton">David Patton</a>
</p>
