"""Fix event_listener.py to respect LiteAgent verbose setting"""

# Read the file
with open(r'd:\test\testing\src\itak\events\event_listener.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix on_lite_agent_execution_started
old_code = '''        @iTaK_event_bus.on(LiteAgentExecutionStartedEvent)
        def on_lite_agent_execution_started(
            _: Any, event: LiteAgentExecutionStartedEvent
        ) -> None:
            """Handle LiteAgent execution started event."""
            self.formatter.handle_lite_agent_execution(
                event.agent_info["role"], status="started", **event.agent_info
            )'''

new_code = '''        @iTaK_event_bus.on(LiteAgentExecutionStartedEvent)
        def on_lite_agent_execution_started(
            _: Any, event: LiteAgentExecutionStartedEvent
        ) -> None:
            """Handle LiteAgent execution started event."""
            # Skip printing if agent has verbose=False
            if not event.agent_info.get("verbose", True):
                return
            self.formatter.handle_lite_agent_execution(
                event.agent_info["role"], status="started", **event.agent_info
            )'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Fixed on_lite_agent_execution_started")
else:
    print("⚠️ Could not find on_lite_agent_execution_started block")

# Also fix on_lite_agent_execution_completed
old_completed = '''        @iTaK_event_bus.on(LiteAgentExecutionCompletedEvent)
        def on_lite_agent_execution_completed(
            _: Any, event: LiteAgentExecutionCompletedEvent
        ) -> None:
            """Handle LiteAgent execution completed event."""
            self.formatter.handle_lite_agent_execution(
                event.agent_info["role"], status="completed", **event.agent_info
            )'''

new_completed = '''        @iTaK_event_bus.on(LiteAgentExecutionCompletedEvent)
        def on_lite_agent_execution_completed(
            _: Any, event: LiteAgentExecutionCompletedEvent
        ) -> None:
            """Handle LiteAgent execution completed event."""
            # Skip printing if agent has verbose=False
            if not event.agent_info.get("verbose", True):
                return
            self.formatter.handle_lite_agent_execution(
                event.agent_info["role"], status="completed", **event.agent_info
            )'''

if old_completed in content:
    content = content.replace(old_completed, new_completed)
    print("✅ Fixed on_lite_agent_execution_completed")
else:
    print("⚠️ Could not find on_lite_agent_execution_completed block")

# Write back
with open(r'd:\test\testing\src\itak\events\event_listener.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ event_listener.py updated")
