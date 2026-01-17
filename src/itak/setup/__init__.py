"""iTaK Setup Package

Handles first-time setup, bootstrap, and auto-deployment of services.
"""

from .bootstrap import main as bootstrap

__all__ = ['bootstrap']
