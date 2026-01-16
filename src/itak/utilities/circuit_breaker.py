"""
iTaK Circuit Breaker - Self-Healing Pattern

Implements the circuit breaker pattern for resilient service calls.
Part of Layer 9 (Healer) - automatic failure detection and recovery.

Based on the metrics.py from iTaK's this.md specification.
"""

import time
import json
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional
from functools import wraps
from dataclasses import dataclass, field


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitStats:
    """Statistics for a circuit breaker."""
    failures: int = 0
    successes: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    total_calls: int = 0
    

@dataclass 
class CircuitBreaker:
    """Circuit breaker implementation for self-healing.
    
    Attributes:
        name: Identifier for this circuit
        failure_threshold: Number of failures before opening
        recovery_timeout: Seconds to wait before testing recovery
        half_open_max_calls: Max calls allowed in half-open state
    """
    name: str
    failure_threshold: int = 3
    recovery_timeout: int = 30
    half_open_max_calls: int = 1
    
    state: CircuitState = field(default=CircuitState.CLOSED)
    stats: CircuitStats = field(default_factory=CircuitStats)
    _half_open_calls: int = field(default=0)
    _opened_at: Optional[datetime] = field(default=None)
    
    def __post_init__(self):
        self.stats = CircuitStats()
        self._half_open_calls = 0
        self._opened_at = None
    
    def can_execute(self) -> bool:
        """Check if the circuit allows execution."""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has elapsed
            if self._opened_at and datetime.now() > self._opened_at + timedelta(seconds=self.recovery_timeout):
                self.state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
                print(f"🔄 [{self.name}] Circuit entering HALF-OPEN state (testing recovery)")
                return True
            return False
        
        if self.state == CircuitState.HALF_OPEN:
            return self._half_open_calls < self.half_open_max_calls
        
        return False
    
    def record_success(self) -> None:
        """Record a successful call."""
        self.stats.successes += 1
        self.stats.total_calls += 1
        self.stats.last_success_time = datetime.now()
        
        if self.state == CircuitState.HALF_OPEN:
            # Service recovered, close the circuit
            self.state = CircuitState.CLOSED
            self.stats.failures = 0
            print(f"✅ [{self.name}] Circuit CLOSED (service recovered)")
    
    def record_failure(self, error: Exception = None) -> None:
        """Record a failed call."""
        self.stats.failures += 1
        self.stats.total_calls += 1
        self.stats.last_failure_time = datetime.now()
        
        if self.state == CircuitState.HALF_OPEN:
            # Failed during recovery test, reopen
            self.state = CircuitState.OPEN
            self._opened_at = datetime.now()
            print(f"🚨 [{self.name}] Circuit OPEN (recovery failed)")
        
        elif self.state == CircuitState.CLOSED:
            if self.stats.failures >= self.failure_threshold:
                self.state = CircuitState.OPEN
                self._opened_at = datetime.now()
                print(f"🚨 [{self.name}] Circuit OPEN ({self.stats.failures} failures)")
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with circuit breaker protection."""
        if not self.can_execute():
            raise CircuitOpenError(f"Circuit '{self.name}' is OPEN - rejecting request")
        
        if self.state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
        
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure(e)
            raise
    
    def reset(self) -> None:
        """Reset the circuit breaker to initial state."""
        self.state = CircuitState.CLOSED
        self.stats = CircuitStats()
        self._half_open_calls = 0
        self._opened_at = None
        print(f"🔄 [{self.name}] Circuit RESET")
    
    def get_status(self) -> dict:
        """Get current circuit status."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failures": self.stats.failures,
            "successes": self.stats.successes,
            "total_calls": self.stats.total_calls,
            "failure_threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout,
        }


class CircuitOpenError(Exception):
    """Raised when circuit is open and rejecting requests."""
    pass


# Global circuit breaker registry
_circuits: dict[str, CircuitBreaker] = {}


def get_circuit(name: str, **kwargs) -> CircuitBreaker:
    """Get or create a named circuit breaker."""
    if name not in _circuits:
        _circuits[name] = CircuitBreaker(name=name, **kwargs)
    return _circuits[name]


def circuit_protected(circuit_name: str, **circuit_kwargs):
    """Decorator to protect a function with a circuit breaker.
    
    Usage:
        @circuit_protected("ollama_api")
        def call_ollama(prompt):
            ...
    """
    def decorator(func: Callable) -> Callable:
        circuit = get_circuit(circuit_name, **circuit_kwargs)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return circuit.execute(func, *args, **kwargs)
        
        wrapper._circuit = circuit
        return wrapper
    
    return decorator


def get_all_circuits() -> dict[str, dict]:
    """Get status of all registered circuits."""
    return {name: circuit.get_status() for name, circuit in _circuits.items()}


def reset_all_circuits() -> None:
    """Reset all circuit breakers."""
    for circuit in _circuits.values():
        circuit.reset()


# System Snapshot functionality (from metrics.py)
@dataclass
class SystemSnapshot:
    """Capture system state for debugging and recovery."""
    timestamp: datetime
    label: str
    metrics: dict
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "label": self.label,
            "metrics": self.metrics,
        }


_snapshots: list[SystemSnapshot] = []
SNAPSHOT_DIR = os.environ.get("ITAK_SNAPSHOT_DIR", "data/snapshots")


def create_snapshot(label: str, metrics: dict = None) -> SystemSnapshot:
    """Create a system snapshot."""
    if metrics is None:
        metrics = {}
    
    # Add circuit breaker states to metrics
    metrics["circuits"] = get_all_circuits()
    
    snapshot = SystemSnapshot(
        timestamp=datetime.now(),
        label=label,
        metrics=metrics,
    )
    
    _snapshots.append(snapshot)
    
    # Save to file
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    filename = f"{SNAPSHOT_DIR}/{snapshot.timestamp.strftime('%Y%m%d_%H%M%S')}_{label}.json"
    with open(filename, 'w') as f:
        json.dump(snapshot.to_dict(), f, indent=2)
    
    print(f"📸 Snapshot created: {label}")
    return snapshot


def get_latest_snapshot() -> Optional[SystemSnapshot]:
    """Get the most recent snapshot."""
    return _snapshots[-1] if _snapshots else None


if __name__ == "__main__":
    # Demo
    @circuit_protected("demo_service", failure_threshold=2, recovery_timeout=5)
    def failing_service():
        raise Exception("Service unavailable")
    
    print("Testing circuit breaker...")
    for i in range(5):
        try:
            failing_service()
        except CircuitOpenError as e:
            print(f"  Request {i+1}: Rejected - {e}")
        except Exception as e:
            print(f"  Request {i+1}: Failed - {e}")
        time.sleep(1)
    
    print("\nCircuit status:", get_all_circuits())
