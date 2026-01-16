import logging

from itak.tools import BaseTool

from itak_tools.adapters.tool_collection import ToolCollection
from itak_tools.tools.iTaK_platform_tools.iTaK_platform_tool_builder import (
    iTaKPlatformToolBuilder,
)


logger = logging.getLogger(__name__)


def iTaKPlatformTools(  # noqa: N802
    apps: list[str],
) -> ToolCollection[BaseTool]:
    """Factory function that returns iTaK platform tools.

    Args:
        apps: List of platform apps to get tools that are available on the platform.

    Returns:
        A list of BaseTool instances for platform actions
    """
    builder = iTaKPlatformToolBuilder(apps=apps)

    return builder.tools()  # type: ignore
