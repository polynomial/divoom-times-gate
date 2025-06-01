"""
Exceptions for Times Gate library.
"""


class TimesGateError(Exception):
    """Base exception for Times Gate errors."""
    pass


class TimesGateConnectionError(TimesGateError):
    """Raised when connection to device fails."""
    pass


class TimesGateCommandError(TimesGateError):
    """Raised when a command fails."""
    pass 