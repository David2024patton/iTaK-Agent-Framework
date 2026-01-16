from itak.events.types.a2a_events import (
    A2AConversationCompletedEvent,
    A2AConversationStartedEvent,
    A2ADelegationCompletedEvent,
    A2ADelegationStartedEvent,
    A2AMessageSentEvent,
    A2APollingStartedEvent,
    A2APollingStatusEvent,
    A2APushNotificationReceivedEvent,
    A2APushNotificationRegisteredEvent,
    A2APushNotificationTimeoutEvent,
    A2AResponseReceivedEvent,
    A2AServerTaskCanceledEvent,
    A2AServerTaskCompletedEvent,
    A2AServerTaskFailedEvent,
    A2AServerTaskStartedEvent,
)
from itak.events.types.agent_events import (
    AgentExecutionCompletedEvent,
    AgentExecutionErrorEvent,
    AgentExecutionStartedEvent,
    LiteAgentExecutionCompletedEvent,
)
from itak.events.types.crew_events import (
    CrewKickoffCompletedEvent,
    CrewKickoffFailedEvent,
    CrewKickoffStartedEvent,
    CrewTestCompletedEvent,
    CrewTestFailedEvent,
    CrewTestStartedEvent,
    CrewTrainCompletedEvent,
    CrewTrainFailedEvent,
    CrewTrainStartedEvent,
)
from itak.events.types.flow_events import (
    FlowFinishedEvent,
    FlowStartedEvent,
    MethodExecutionFailedEvent,
    MethodExecutionFinishedEvent,
    MethodExecutionStartedEvent,
)
from itak.events.types.knowledge_events import (
    KnowledgeQueryCompletedEvent,
    KnowledgeQueryFailedEvent,
    KnowledgeQueryStartedEvent,
    KnowledgeRetrievalCompletedEvent,
    KnowledgeRetrievalStartedEvent,
    KnowledgeSearchQueryFailedEvent,
)
from itak.events.types.llm_events import (
    LLMCallCompletedEvent,
    LLMCallFailedEvent,
    LLMCallStartedEvent,
    LLMStreamChunkEvent,
)
from itak.events.types.llm_guardrail_events import (
    LLMGuardrailCompletedEvent,
    LLMGuardrailStartedEvent,
)
from itak.events.types.mcp_events import (
    MCPConnectionCompletedEvent,
    MCPConnectionFailedEvent,
    MCPConnectionStartedEvent,
    MCPToolExecutionCompletedEvent,
    MCPToolExecutionFailedEvent,
    MCPToolExecutionStartedEvent,
)
from itak.events.types.memory_events import (
    MemoryQueryCompletedEvent,
    MemoryQueryFailedEvent,
    MemoryQueryStartedEvent,
    MemoryRetrievalCompletedEvent,
    MemoryRetrievalStartedEvent,
    MemorySaveCompletedEvent,
    MemorySaveFailedEvent,
    MemorySaveStartedEvent,
)
from itak.events.types.reasoning_events import (
    AgentReasoningCompletedEvent,
    AgentReasoningFailedEvent,
    AgentReasoningStartedEvent,
)
from itak.events.types.task_events import (
    TaskCompletedEvent,
    TaskFailedEvent,
    TaskStartedEvent,
)
from itak.events.types.tool_usage_events import (
    ToolUsageErrorEvent,
    ToolUsageFinishedEvent,
    ToolUsageStartedEvent,
)


EventTypes = (
    A2AConversationCompletedEvent
    | A2AConversationStartedEvent
    | A2ADelegationCompletedEvent
    | A2ADelegationStartedEvent
    | A2AMessageSentEvent
    | A2APollingStartedEvent
    | A2APollingStatusEvent
    | A2APushNotificationReceivedEvent
    | A2APushNotificationRegisteredEvent
    | A2APushNotificationTimeoutEvent
    | A2AResponseReceivedEvent
    | A2AServerTaskCanceledEvent
    | A2AServerTaskCompletedEvent
    | A2AServerTaskFailedEvent
    | A2AServerTaskStartedEvent
    | CrewKickoffStartedEvent
    | CrewKickoffCompletedEvent
    | CrewKickoffFailedEvent
    | CrewTestStartedEvent
    | CrewTestCompletedEvent
    | CrewTestFailedEvent
    | CrewTrainStartedEvent
    | CrewTrainCompletedEvent
    | CrewTrainFailedEvent
    | AgentExecutionStartedEvent
    | AgentExecutionCompletedEvent
    | LiteAgentExecutionCompletedEvent
    | TaskStartedEvent
    | TaskCompletedEvent
    | TaskFailedEvent
    | FlowStartedEvent
    | FlowFinishedEvent
    | MethodExecutionStartedEvent
    | MethodExecutionFinishedEvent
    | MethodExecutionFailedEvent
    | AgentExecutionErrorEvent
    | ToolUsageFinishedEvent
    | ToolUsageErrorEvent
    | ToolUsageStartedEvent
    | LLMCallStartedEvent
    | LLMCallCompletedEvent
    | LLMCallFailedEvent
    | LLMStreamChunkEvent
    | LLMGuardrailStartedEvent
    | LLMGuardrailCompletedEvent
    | AgentReasoningStartedEvent
    | AgentReasoningCompletedEvent
    | AgentReasoningFailedEvent
    | KnowledgeRetrievalStartedEvent
    | KnowledgeRetrievalCompletedEvent
    | KnowledgeQueryStartedEvent
    | KnowledgeQueryCompletedEvent
    | KnowledgeQueryFailedEvent
    | KnowledgeSearchQueryFailedEvent
    | MemorySaveStartedEvent
    | MemorySaveCompletedEvent
    | MemorySaveFailedEvent
    | MemoryQueryStartedEvent
    | MemoryQueryCompletedEvent
    | MemoryQueryFailedEvent
    | MemoryRetrievalStartedEvent
    | MemoryRetrievalCompletedEvent
    | MCPConnectionStartedEvent
    | MCPConnectionCompletedEvent
    | MCPConnectionFailedEvent
    | MCPToolExecutionStartedEvent
    | MCPToolExecutionCompletedEvent
    | MCPToolExecutionFailedEvent
)
