"""Test iTaK telemetry to VPS.

This script creates a simple crew and runs it to verify that
telemetry data is being sent to the VPS at 145.79.2.67:4318.
"""

from itak import Agent, Crew, Task

# Create a simple agent
test_agent = Agent(
    role="Telemetry Tester",
    goal="Verify that telemetry is working correctly",
    backstory="You are a test agent designed to verify telemetry functionality.",
    verbose=True
)

# Create a simple task
test_task = Task(
    description="Say hello and confirm telemetry is working",
    expected_output="A simple greeting message",
    agent=test_agent
)

# Create a crew
test_crew = Crew(
    agents=[test_agent],
    tasks=[test_task],
    verbose=True
)

# Run the crew
print("=" * 60)
print("STARTING TELEMETRY TEST")
print("=" * 60)
print(f"Telemetry will be sent to: 145.79.2.67:4318/v1/traces")
print("=" * 60)

result = test_crew.kickoff()

print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print(f"Result: {result}")
print("=" * 60)
print("\nCheck Grafana at http://145.79.2.67:3456/")
print("Go to Explore -> Tempo -> Search for service.name = 'itak-telemetry'")
print("=" * 60)
