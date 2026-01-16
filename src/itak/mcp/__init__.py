"""MCP (Model Context Protocol) client support for iTaK agents.

This module provides native MCP client functionality, allowing iTaK agents
to connect to any MCP-compliant server using various transport types.
"""

from itak.mcp.client import MCPClient
from itak.mcp.config import (
    MCPServerConfig,
    MCPServerHTTP,
    MCPServerSSE,
    MCPServerStdio,
)
from itak.mcp.filters import (
    StaticToolFilter,
    ToolFilter,
    ToolFilterContext,
    create_dynamic_tool_filter,
    create_static_tool_filter,
)
from itak.mcp.transports.base import BaseTransport, TransportType


__all__ = [
    "BaseTransport",
    "MCPClient",
    "MCPServerConfig",
    "MCPServerHTTP",
    "MCPServerSSE",
    "MCPServerStdio",
    "StaticToolFilter",
    "ToolFilter",
    "ToolFilterContext",
    "TransportType",
    "create_dynamic_tool_filter",
    "create_static_tool_filter",
]
