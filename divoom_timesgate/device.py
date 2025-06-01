"""
Times Gate Device Control

Main class for controlling Divoom Times Gate devices.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging

from .exceptions import TimesGateError, TimesGateConnectionError, TimesGateCommandError
from .models import DisplayPanel, TextAlignment, FontSize, TemperatureMode, TimeFormat

logger = logging.getLogger(__name__)


class TimesGateDevice:
    """Main class for controlling a Divoom Times Gate device."""
    
    def __init__(self, ip_address: str, port: int = 80):
        """
        Initialize a Times Gate device connection.
        
        Args:
            ip_address: IP address of the device
            port: HTTP port (default: 80)
        """
        self.ip_address = ip_address
        self.port = port
        self.base_url = f"http://{ip_address}:{port}/post"
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def connect(self):
        """Initialize the HTTP session."""
        if not self._session:
            self._session = aiohttp.ClientSession()
    
    async def close(self):
        """Close the HTTP session."""
        if self._session:
            await self._session.close()
            self._session = None
    
    async def _send_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a command to the device.
        
        Args:
            command: Command dictionary to send
            
        Returns:
            Response from the device
            
        Raises:
            TimesGateConnectionError: If connection fails
            TimesGateCommandError: If command fails
        """
        if not self._session:
            await self.connect()
        
        try:
            logger.debug(f"Sending command to {self.ip_address}: {json.dumps(command)}")
            
            async with self._session.post(
                self.base_url,
                json=command,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                # Get response as text first (device returns text/html content type)
                response_text = await response.text()
                
                try:
                    response_data = json.loads(response_text)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON response: {response_text}")
                    raise TimesGateCommandError(f"Invalid JSON response from device")
                
                logger.debug(f"Response from {self.ip_address}: {json.dumps(response_data)}")
                
                if response_data.get("error_code", 0) != 0:
                    raise TimesGateCommandError(
                        f"Command failed with error code: {response_data.get('error_code')}"
                    )
                
                return response_data
                
        except aiohttp.ClientError as e:
            raise TimesGateConnectionError(f"Failed to connect to device: {str(e)}")
    
    # System Settings
    
    async def set_brightness(self, brightness: int) -> bool:
        """
        Set the display brightness.
        
        Args:
            brightness: Brightness level (0-100)
            
        Returns:
            True if successful
        """
        if not 0 <= brightness <= 100:
            raise ValueError("Brightness must be between 0 and 100")
        
        await self._send_command({
            "Command": "Channel/SetBrightness",
            "Brightness": brightness
        })
        return True
    
    async def get_settings(self) -> Dict[str, Any]:
        """
        Get all device settings.
        
        Returns:
            Dictionary of device settings
        """
        response = await self._send_command({
            "Command": "Channel/GetAllConf"
        })
        return response
    
    async def set_device_time(self, timestamp: Optional[int] = None) -> bool:
        """
        Set the device time.
        
        Args:
            timestamp: Unix timestamp (default: current time)
            
        Returns:
            True if successful
        """
        if timestamp is None:
            timestamp = int(datetime.now().timestamp())
        
        await self._send_command({
            "Command": "Device/SetUTC",
            "Utc": timestamp
        })
        return True
    
    async def get_device_time(self) -> Dict[str, Any]:
        """
        Get the device time.
        
        Returns:
            Dictionary with UTC time and local time
        """
        response = await self._send_command({
            "Command": "Device/GetDeviceTime"
        })
        return response
    
    async def set_timezone(self, timezone: str) -> bool:
        """
        Set the device timezone.
        
        Args:
            timezone: Timezone string (e.g., "GMT-5", "GMT+8")
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Sys/TimeZone",
            "TimeZoneValue": timezone
        })
        return True
    
    async def set_temperature_mode(self, mode: TemperatureMode) -> bool:
        """
        Set temperature display mode.
        
        Args:
            mode: Temperature mode (Celsius or Fahrenheit)
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Device/SetDisTempMode",
            "Mode": mode.value
        })
        return True
    
    async def set_mirror_mode(self, enabled: bool) -> bool:
        """
        Set display mirror mode.
        
        Args:
            enabled: True to enable mirroring
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Device/SetMirrorMode",
            "Mode": 1 if enabled else 0
        })
        return True
    
    async def set_time_format(self, format: TimeFormat) -> bool:
        """
        Set time display format.
        
        Args:
            format: Time format (12-hour or 24-hour)
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Device/SetTime24Flag",
            "Mode": format.value
        })
        return True
    
    async def set_screen_power(self, on: bool) -> bool:
        """
        Turn the display on or off.
        
        Args:
            on: True to turn on, False to turn off
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Channel/OnOffScreen",
            "OnOff": 1 if on else 0
        })
        return True
    
    async def set_weather_location(self, latitude: float, longitude: float) -> bool:
        """
        Set the weather location.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Sys/LogAndLat",
            "Latitude": str(latitude),
            "Longitude": str(longitude)
        })
        return True
    
    async def reboot(self) -> bool:
        """
        Reboot the device.
        
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Device/Reboot"
        })
        return True
    
    # Display Control
    
    async def get_channel_info(self) -> Dict[str, Any]:
        """
        Get current channel information.
        
        Returns:
            Dictionary with channel information
        """
        response = await self._send_command({
            "Command": "Channel/GetCurChannelInfo"
        })
        return response
    
    async def set_whole_dial(self, clock_id: int) -> bool:
        """
        Set clock face for all displays.
        
        Args:
            clock_id: ID of the clock face
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Channel/SetWholeDial",
            "ClockId": clock_id
        })
        return True
    
    async def set_individual_dial(self, panel: DisplayPanel, clock_id: int) -> bool:
        """
        Set clock face for individual LCD panel.
        
        Args:
            panel: Display panel
            clock_id: ID of the clock face
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Channel/SetIndividualDial",
            "LcdId": panel.value,
            "ClockId": clock_id
        })
        return True
    
    async def get_dial_list(self) -> List[Dict[str, Any]]:
        """
        Get available clock faces.
        
        Returns:
            List of available clock faces
        """
        response = await self._send_command({
            "Command": "Channel/GetWholeDial"
        })
        return response.get("ClockList", [])
    
    # Animation & Text
    
    async def send_text(
        self,
        text: str,
        text_id: int = 1,
        x: int = 0,
        y: int = 0,
        color: str = "#FFFFFF",
        font: FontSize = FontSize.MEDIUM,
        alignment: TextAlignment = TextAlignment.CENTER,
        scroll_speed: int = 0,
        direction: int = 0,
        width: int = 64
    ) -> bool:
        """
        Display text on the device.
        
        Args:
            text: Text to display
            text_id: Unique text ID (0-19)
            x: X position
            y: Y position
            color: Hex color (#RRGGBB)
            font: Font size
            alignment: Text alignment
            scroll_speed: Scroll speed (0-100, 0=static)
            direction: Scroll direction (0=left, 1=right)
            width: Text area width
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Draw/SendHttpText",
            "TextId": text_id,
            "x": x,
            "y": y,
            "dir": direction,
            "font": font.value,
            "TextWidth": width,
            "TextString": text,
            "speed": scroll_speed,
            "color": color,
            "align": alignment.value
        })
        return True
    
    async def clear_text(self, text_id: int = -1) -> bool:
        """
        Clear displayed text.
        
        Args:
            text_id: Text ID to clear (-1 for all)
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Draw/ClearHttpText",
            "TextId": text_id
        })
        return True
    
    async def play_gif(self, url: str) -> bool:
        """
        Play a GIF animation from URL.
        
        Args:
            url: URL of the GIF file
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Device/PlayTFGif",
            "FileType": 2,
            "FileName": url
        })
        return True
    
    async def get_font_list(self) -> List[Dict[str, Any]]:
        """
        Get available fonts.
        
        Returns:
            List of available fonts
        """
        response = await self._send_command({
            "Command": "Device/GetFontList"
        })
        return response.get("FontList", [])
    
    # Tools
    
    async def set_countdown(self, minutes: int, seconds: int, start: bool = True) -> bool:
        """
        Set countdown timer.
        
        Args:
            minutes: Minutes (0-99)
            seconds: Seconds (0-59)
            start: True to start, False to stop
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Tools/SetTimer",
            "Minute": minutes,
            "Second": seconds,
            "Status": 1 if start else 0
        })
        return True
    
    async def set_stopwatch(self, start: bool) -> bool:
        """
        Control the stopwatch.
        
        Args:
            start: True to start, False to stop/reset
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Tools/SetStopWatch",
            "Status": 1 if start else 0
        })
        return True
    
    async def set_scoreboard(self, red_score: int, blue_score: int) -> bool:
        """
        Display a scoreboard.
        
        Args:
            red_score: Red team score (0-999)
            blue_score: Blue team score (0-999)
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Tools/SetScoreBoard",
            "RedScore": red_score,
            "BlueScore": blue_score
        })
        return True
    
    async def set_noise_meter(self, enabled: bool) -> bool:
        """
        Enable or disable noise meter.
        
        Args:
            enabled: True to enable
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Tools/SetNoiseStatus",
            "Status": 1 if enabled else 0
        })
        return True
    
    async def play_buzzer(
        self,
        on_time: int = 500,
        off_time: int = 500,
        total_time: int = 2000
    ) -> bool:
        """
        Sound the buzzer.
        
        Args:
            on_time: Buzzer on time in ms
            off_time: Buzzer off time in ms
            total_time: Total duration in ms
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Device/PlayBuzzer",
            "ActiveTimeInCycle": on_time,
            "OffTimeInCycle": off_time,
            "PlayTotalTime": total_time
        })
        return True
    
    # Advanced Features
    
    async def send_command_list(self, commands: List[Dict[str, Any]]) -> bool:
        """
        Execute multiple commands in sequence.
        
        Args:
            commands: List of command dictionaries
            
        Returns:
            True if successful
        """
        await self._send_command({
            "Command": "Draw/CommandList",
            "CommandList": commands
        })
        return True
    
    async def send_raw_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a raw command to the device.
        
        Args:
            command: Command dictionary
            
        Returns:
            Response from the device
        """
        return await self._send_command(command) 