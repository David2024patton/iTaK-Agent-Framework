"""Base event listener for iTaK event system."""

from abc import ABC, abstractmethod

from itak.events.event_bus import iTaKEventsBus, iTaK_event_bus


class BaseEventListener(ABC):
    """Abstract base class for event listeners."""

    verbose: bool = False

    def __init__(self) -> None:
        """Initialize the event listener and register handlers."""
        super().__init__()
        self.setup_listeners(iTaK_event_bus)
        iTaK_event_bus.validate_dependencies()

    @abstractmethod
    def setup_listeners(self, iTaK_event_bus: iTaKEventsBus) -> None:
        """Setup event listeners on the event bus.

        Args:
            iTaK_event_bus: The event bus to register listeners on.
        """
        pass
