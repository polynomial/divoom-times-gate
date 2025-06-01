"""
Divoom Times Gate Python Library

A comprehensive Python library for controlling Divoom Times Gate devices.
"""

from .device import TimesGateDevice
from .discovery import discover_devices
from .exceptions import TimesGateError, TimesGateConnectionError, TimesGateCommandError
from .models import (
    DisplayPanel,
    TextAlignment,
    FontSize,
    DisplayType,
    TemperatureMode,
    TimeFormat
)

__version__ = "1.0.0"
__author__ = "Divoom Times Gate Community"

__all__ = [
    "TimesGateDevice",
    "discover_devices",
    "TimesGateError",
    "TimesGateConnectionError",
    "TimesGateCommandError",
    "DisplayPanel",
    "TextAlignment",
    "FontSize",
    "DisplayType",
    "TemperatureMode",
    "TimeFormat"
] 