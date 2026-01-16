import threading
from typing import Any
import urllib.request
import warnings

from itak.agent.core import Agent
from itak.crew import Crew
from itak.crews.crew_output import CrewOutput
from itak.flow.flow import Flow
from itak.knowledge.knowledge import Knowledge
from itak.llm import LLM
from itak.llms.base_llm import BaseLLM
from itak.process import Process
from itak.task import Task
from itak.tasks.llm_guardrail import LLMGuardrail
from itak.tasks.task_output import TaskOutput
from itak.telemetry.telemetry import Telemetry


def _suppress_pydantic_deprecation_warnings() -> None:
    """Suppress Pydantic deprecation warnings using targeted monkey patch."""
    original_warn = warnings.warn

    def filtered_warn(
        message: Any,
        category: type | None = None,
        stacklevel: int = 1,
        source: Any = None,
    ) -> Any:
        if (
            category
            and hasattr(category, "__module__")
            and category.__module__ == "pydantic.warnings"
        ):
            return None
        return original_warn(message, category, stacklevel + 1, source)

    warnings.warn = filtered_warn  # type: ignore[assignment]


_suppress_pydantic_deprecation_warnings()

__version__ = "0.1.0"  # iTaK initial version
_telemetry_submitted = False


def _track_install() -> None:
    """Track package installation/first-use via Scarf analytics."""
    global _telemetry_submitted

    if _telemetry_submitted or Telemetry._is_telemetry_disabled():
        return

    try:
        pixel_url = "https://api.scarf.sh/v2/packages/iTaK/iTaK/docs/00f2dad1-8334-4a39-934e-003b2e1146db"

        req = urllib.request.Request(pixel_url)  # noqa: S310
        req.add_header("User-Agent", f"iTaK-Python/{__version__}")

        with urllib.request.urlopen(req, timeout=2):  # noqa: S310
            _telemetry_submitted = True
    except Exception:  # noqa: S110
        pass


def _track_install_async() -> None:
    """Track installation in background thread to avoid blocking imports."""
    if not Telemetry._is_telemetry_disabled():
        thread = threading.Thread(target=_track_install, daemon=True)
        thread.start()


_track_install_async()
__all__ = [
    "LLM",
    "Agent",
    "BaseLLM",
    "Crew",
    "CrewOutput",
    "Flow",
    "Knowledge",
    "LLMGuardrail",
    "Process",
    "Task",
    "TaskOutput",
    "__version__",
]
