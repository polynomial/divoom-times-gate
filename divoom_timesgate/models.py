"""
Data models and enums for Times Gate devices.
"""

from enum import Enum


class DisplayPanel(Enum):
    """LCD panel positions on the Times Gate."""
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4
    CENTER = 5


class TextAlignment(Enum):
    """Text alignment options."""
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class FontSize(Enum):
    """Available font sizes."""
    TINY = 0    # 5px
    SMALL = 1   # 8px
    MEDIUM = 2  # 11px
    LARGE = 3   # 14px
    HUGE = 4    # 16px


class DisplayType(Enum):
    """Display item types for display lists."""
    CENTER = 6
    DATE_TIME = 14
    CUSTOM_TEXT = 22
    DYNAMIC_URL_TEXT = 23


class TemperatureMode(Enum):
    """Temperature display modes."""
    CELSIUS = 0
    FAHRENHEIT = 1


class TimeFormat(Enum):
    """Time display formats."""
    HOUR_12 = 0
    HOUR_24 = 1 