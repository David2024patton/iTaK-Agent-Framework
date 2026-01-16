# iTaK Agent Framework

### Intelligent Task Automation Kernel

A powerful multi-agent automation framework built for autonomous task execution with self-healing capabilities.

## Features

- **10-Layer Architecture** - Analyst, Recon, Orchestrator, Builder, Validator, Sandbox, Deployer, Librarian, Healer, Swarm
- **Self-Healing** - Circuit breaker pattern with automatic recovery
- **Persistent Memory** - ChromaDB-based semantic memory
- **Local-First** - Optimized for Ollama and local LLMs
- **Docker Sandbox** - Safe code execution environment
- **Training Data** - Logs all LLM interactions for fine-tuning

## Quick Start

```bash
pip install itak
```

```python
from itak import Agent, Crew, Task

analyst = Agent(
    role="Senior Analyst",
    goal="Analyze requirements and create plans"
)

task = Task(
    description="Analyze the project requirements",
    agent=analyst
)

crew = Crew(agents=[analyst], tasks=[task])
result = crew.kickoff()
```

## CLI Usage

```bash
# Create a new project
itak create crew my-project

# Run the crew
itak run
```

## 10-Layer Architecture

| Layer | Role | Purpose |
|:-----:|------|---------|
| 1 | Analyst | Parse intent, gather requirements |
| 2 | Recon | Research, web scraping, data gathering |
| 3 | Orchestrator | Plan and delegate work |
| 4 | Builder | Write code and content |
| 5 | Validator | Test, lint, verify quality |
| 6 | Sandbox | Execute code safely in Docker |
| 7 | Deployer | Deploy to production |
| 8 | Librarian | Manage memory and skills |
| 9 | Healer | Monitor, detect failures, auto-recover |
| 10 | Swarm | Multi-agent collaboration |

## Ollama Configuration

```python
from itak import LLM

llm = LLM(
    model="ollama/qwen3:4b",
    base_url="http://localhost:11434"
)
```

## Acknowledgments

iTaK Agent Framework is built upon [itak](https://github.com/itakInc/itak), licensed under the MIT License. We thank the itak team for their foundational work.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

*Created by David Patton*
