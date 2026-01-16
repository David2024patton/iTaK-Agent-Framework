"""
iTaK security module.

This module provides security-related functionality for iTaK, including:
- Fingerprinting for component identity and tracking
- Security configuration for controlling access and permissions
- Future: authentication, scoping, and delegation mechanisms
"""

from itak.security.fingerprint import Fingerprint
from itak.security.security_config import SecurityConfig


__all__ = ["Fingerprint", "SecurityConfig"]
