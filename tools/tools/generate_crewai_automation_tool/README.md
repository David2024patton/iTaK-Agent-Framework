# GenerateitakAutomationTool

## Description

The GenerateitakAutomationTool integrates with itak Studio API to generate complete itak automations from natural language descriptions. It translates high-level requirements into functional itak implementations and returns direct links to Studio projects.

## Environment Variables

Set your itak Personal Access Token (itak AMP > Settings > Account > Personal Access Token):

```bash
export itak_PERSONAL_ACCESS_TOKEN="your_personal_access_token_here"
export itak_PLUS_URL="https://app.itak.com"  # optional
```

## Example

```python
from itak_tools import GenerateitakAutomationTool
from itak import Agent, Task, Crew

# Initialize tool
tool = GenerateitakAutomationTool()

# Generate automation
result = tool.run(
    prompt="Generate a itak automation that scrapes websites and stores data in a database",
    organization_id="org_123"  # optional but recommended
)

print(result)
# Output: Generated itak Studio project URL: https://studio.itak.com/project/abc123

# Use with agent
agent = Agent(
    role="Automation Architect",
    goal="Generate itak automations",
    backstory="Expert at creating automated workflows",
    tools=[tool]
)

task = Task(
    description="Create a lead qualification automation",
    agent=agent,
    expected_output="Studio project URL"
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```
