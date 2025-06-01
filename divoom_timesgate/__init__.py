"""
Divoom Times Gate Python Library

Modern async Python library for controlling Divoom Times Gate devices.
"""

from .device import TimesGateDevice
from .exceptions import TimesGateError, TimesGateConnectionError, TimesGateCommandError
from .models import (
    DisplayPanel,
    TextAlignment,
    FontSize,
    TemperatureMode,
    TimeFormat,
    DisplayItemType,
    DisplayItem,
    TextDisplayItem,
    DateTimeDisplayItem
)

__version__ = "1.0.0"
__author__ = "Divoom Times Gate Community"

__all__ = [
    # Main device class
    "TimesGateDevice",
    
    # Exceptions
    "TimesGateError",
    "TimesGateConnectionError",
    "TimesGateCommandError",
    
    # Enums
    "DisplayPanel",
    "TextAlignment",
    "FontSize",
    "TemperatureMode",
    "TimeFormat",
    "DisplayItemType",
    
    # Display Items
    "DisplayItem",
    "TextDisplayItem",
    "DateTimeDisplayItem"
] 