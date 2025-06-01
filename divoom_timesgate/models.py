"""
Data models and enums for Times Gate devices.
"""

from enum import Enum, IntEnum
from typing import Dict, Any


class DisplayPanel(IntEnum):
    """LCD panel positions on the Times Gate."""
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4
    CENTER = 5


class TextAlignment(IntEnum):
    """Text alignment options."""
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class FontSize(IntEnum):
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


class TemperatureMode(IntEnum):
    """Temperature display modes."""
    CELSIUS = 0
    FAHRENHEIT = 1


class TimeFormat(IntEnum):
    """Time display formats."""
    HOUR_12 = 0
    HOUR_24 = 1


class DisplayItemType(IntEnum):
    """Display item types for display lists."""
    TEMPERATURE = 5
    CENTER_ITEM = 6
    TOP_LEFT_ITEM = 14
    CUSTOM_TEXT = 22
    DATE_TIME = 23
    WEATHER = 24


class DisplayItem:
    """Base class for display items."""
    
    def __init__(self, text_id: int, x: int = 0, y: int = 0):
        self.text_id = text_id
        self.x = x
        self.y = y
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API dictionary format."""
        raise NotImplementedError


class TextDisplayItem(DisplayItem):
    """Custom text display item."""
    
    def __init__(
        self,
        text_id: int,
        text: str,
        x: int = 0,
        y: int = 0,
        color: str = "#FFFFFF",
        font: int = 2,
        width: int = 64,
        height: int = 16,
        speed: int = 0,
        align: int = 1,
        direction: int = 0
    ):
        super().__init__(text_id, x, y)
        self.text = text
        self.color = color
        self.font = font
        self.width = width
        self.height = height
        self.speed = speed
        self.align = align
        self.direction = direction
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API dictionary format."""
        return {
            "TextId": self.text_id,
            "type": DisplayItemType.CUSTOM_TEXT.value,
            "x": self.x,
            "y": self.y,
            "dir": self.direction,
            "font": self.font,
            "TextWidth": self.width,
            "Textheight": self.height,
            "speed": self.speed,
            "align": self.align,
            "TextString": self.text,
            "color": self.color
        }


class DateTimeDisplayItem(DisplayItem):
    """Date/time display item."""
    
    def __init__(
        self,
        text_id: int,
        x: int = 0,
        y: int = 48,
        color: str = "#FFF000",
        font: int = 4,
        width: int = 64,
        height: int = 16,
        update_time: int = 60,
        url: str = "http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0"
    ):
        super().__init__(text_id, x, y)
        self.color = color
        self.font = font
        self.width = width
        self.height = height
        self.update_time = update_time
        self.url = url
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API dictionary format."""
        return {
            "TextId": self.text_id,
            "type": DisplayItemType.DATE_TIME.value,
            "x": self.x,
            "y": self.y,
            "dir": 0,
            "font": self.font,
            "TextWidth": self.width,
            "Textheight": self.height,
            "speed": 100,
            "update_time": self.update_time,
            "align": 1,
            "TextString": self.url,
            "color": self.color
        }


TIMER = 50
STOPWATCH = 51
SCOREBOARD = 52
CUSTOM = 99 