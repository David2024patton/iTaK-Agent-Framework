"""Telemetry configuration constants.

This module defines constants used for iTaK telemetry configuration.
Telemetry is now local-first - data goes to YOUR server, not CrewAI's.
"""

import os
from typing import Final


# Default to VPS telemetry server - override with ITAK_TELEMETRY_URL env var
iTaK_TELEMETRY_BASE_URL: Final[str] = os.getenv(
    "ITAK_TELEMETRY_URL", 
    "http://145.79.2.67:4319"  # iTaK VPS OTLP collector
)
iTaK_TELEMETRY_SERVICE_NAME: Final[str] = "itak-telemetry"

