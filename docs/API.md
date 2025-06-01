# Divoom Times Gate API Reference

This document provides a complete reference for the Divoom Times Gate Python API. The API communicates with the device via HTTP POST requests to port 80.

## Table of Contents

- [Connection Setup](#connection-setup)
- [Display Control](#display-control)
- [System Configuration](#system-configuration)
- [Tools and Utilities](#tools-and-utilities)
- [Animation and Graphics](#animation-and-graphics)
- [Data Types and Constants](#data-types-and-constants)

## Connection Setup

### Initialize Device Connection

```python
from src.divoom_times_gate import DivoomTimesGate

# Uses DIVOOM_TIMES_GATE_IP environment variable
device = DivoomTimesGate()

# Or specify IP directly
device = DivoomTimesGate()
device.ip = "192.168.1.100"
```

## Display Control

### set_brightness(brightness)

Set the display brightness.

**Parameters:**
- `brightness` (int): Brightness level from 0 to 100

**Example:**
```python
device.set_brightness(75)  # Set to 75% brightness
```

### switch_screen(onoff)

Turn the display on or off.

**Parameters:**
- `onoff` (int): 1 to turn on, 0 to turn off

**Example:**
```python
device.switch_screen(1)  # Turn on
device.switch_screen(0)  # Turn off
```

### send_display_list(lcd_index, new_flag, background_gif, item_list)

Send a complex display configuration with multiple items.

**Parameters:**
- `lcd_index` (int): LCD panel index (1-5)
- `new_flag` (int): 1 for new display, 0 to update existing
- `background_gif` (str): URL or path to background GIF
- `item_list` (list): List of display items (see Display Item Types)

**Example:**
```python
items = [
    {
        "TextId": 1,
        "type": 22,  # Custom text
        "x": 10, "y": 10,
        "TextString": "Hello World",
        "color": "#FFFFFF",
        "font": 2,
        "TextWidth": 48,
        "speed": 100,
        "align": 1
    }
]
device.send_display_list(1, 1, "http://example.com/bg.gif", items)
```

### send_text(lcd_index, text_id, x, y, dir, font, text_width, text_string, speed, color, align)

Display text on the screen.

**Parameters:**
- `lcd_index` (int): LCD panel index
- `text_id` (int): Unique text identifier
- `x` (int): X coordinate (0-63)
- `y` (int): Y coordinate (0-63)
- `dir` (int): Direction (0=left-to-right, 1=top-to-bottom)
- `font` (int): Font ID (see Font Types)
- `text_width` (int): Text display width
- `text_string` (str): Text to display
- `speed` (int): Scroll speed (0-100)
- `color` (str): Hex color code (e.g., "#FF0000")
- `align` (int): Alignment (1=left, 2=center, 3=right)

**Example:**
```python
device.send_text(
    lcd_index=1,
    text_id=1,
    x=5, y=20,
    dir=0,
    font=4,
    text_width=54,
    text_string="Temperature: 72°F",
    speed=0,  # Static text
    color="#00FF00",
    align=2  # Center aligned
)
```

## System Configuration

### get_all_settings()

Get all current device settings.

**Returns:** Dictionary with all device settings

**Example:**
```python
settings = device.get_all_settings()
print(settings)
```

### set_timezone(timezone)

Set the device timezone.

**Parameters:**
- `timezone` (str): Timezone string (e.g., "GMT-8:00")

**Example:**
```python
device.set_timezone("GMT-8:00")  # Pacific Time
```

### set_weather_location(longitude, latitude)

Set location for weather information.

**Parameters:**
- `longitude` (float): Longitude coordinate
- `latitude` (float): Latitude coordinate

**Example:**
```python
# San Francisco coordinates
device.set_weather_location(-122.4194, 37.7749)
```

### set_system_time(utc)

Set the system time using UTC timestamp.

**Parameters:**
- `utc` (int): UTC timestamp

**Example:**
```python
import time
device.set_system_time(int(time.time()))
```

### get_device_time()

Get the current device time.

**Returns:** Dictionary with current time information

### set_temperature_mode(mode)

Set temperature display mode.

**Parameters:**
- `mode` (int): 0 for Celsius, 1 for Fahrenheit

**Example:**
```python
device.set_temperature_mode(0)  # Use Celsius
```

### set_mirror_mode(mode)

Enable or disable mirror mode.

**Parameters:**
- `mode` (int): 1 to enable, 0 to disable

### set_hour_mode(mode)

Set 12/24 hour time format.

**Parameters:**
- `mode` (int): 1 for 24-hour, 0 for 12-hour

**Example:**
```python
device.set_hour_mode(1)  # Use 24-hour format
```

### get_weather()

Get current weather information.

**Returns:** Dictionary with weather data

**Example:**
```python
weather = device.get_weather()
print(f"Temperature: {weather['temperature']}°")
print(f"Conditions: {weather['conditions']}")
```

## Tools and Utilities

### set_countdown_tool(minutes, seconds, status)

Control the countdown timer.

**Parameters:**
- `minutes` (int): Minutes (0-99)
- `seconds` (int): Seconds (0-59)
- `status` (int): 1 to start, 0 to stop

**Example:**
```python
# Start 5-minute timer
device.set_countdown_tool(5, 0, 1)

# Stop timer
device.set_countdown_tool(0, 0, 0)
```

### set_stopwatch_tool(status)

Control the stopwatch.

**Parameters:**
- `status` (int): 1=start, 2=stop, 3=reset

**Example:**
```python
device.set_stopwatch_tool(1)  # Start
device.set_stopwatch_tool(2)  # Stop
device.set_stopwatch_tool(3)  # Reset
```

### set_scoreboard_tool(blue_score, red_score)

Display a scoreboard.

**Parameters:**
- `blue_score` (int): Blue team score (0-999)
- `red_score` (int): Red team score (0-999)

**Example:**
```python
device.set_scoreboard_tool(15, 12)
```

### set_noise_tool(status)

Control the noise level meter.

**Parameters:**
- `status` (int): 1 to start, 0 to stop

### play_buzzer(active_time, off_time, total_time)

Play the device buzzer.

**Parameters:**
- `active_time` (int): Buzzer on time in milliseconds
- `off_time` (int): Buzzer off time in milliseconds
- `total_time` (int): Total duration in milliseconds

**Example:**
```python
# Beep pattern: 100ms on, 100ms off, for 1 second
device.play_buzzer(100, 100, 1000)
```

## Animation and Graphics

### play_gif(file_names, lcd_array)

Play GIF animations on specified LCD panels.

**Parameters:**
- `file_names` (list): List of GIF file paths/URLs
- `lcd_array` (list): List of LCD panel indices

**Example:**
```python
device.play_gif(
    ["animation1.gif", "animation2.gif"],
    [1, 2]  # Play on panels 1 and 2
)
```

### play_gif_in_all_lcds(lcd_files)

Play different GIFs on each LCD panel.

**Parameters:**
- `lcd_files` (list): List of file paths for each LCD

**Example:**
```python
device.play_gif_in_all_lcds([
    "lcd1.gif",
    "lcd2.gif",
    "lcd3.gif",
    "lcd4.gif",
    "lcd5.gif"
])
```

### play_divoom_gif(file_id, lcd_array)

Play a GIF from Divoom's server.

**Parameters:**
- `file_id` (str): Divoom server file ID
- `lcd_array` (list): LCD panels to display on

### send_animation(pic_num, pic_width, pic_offset, pic_id, pic_speed, pic_data, lcd_array)

Send custom animation frames.

**Parameters:**
- `pic_num` (int): Number of frames
- `pic_width` (int): Frame width in pixels
- `pic_offset` (int): Starting offset
- `pic_id` (int): Animation ID
- `pic_speed` (int): Animation speed (ms per frame)
- `pic_data` (str): Base64 encoded frame data
- `lcd_array` (list): LCD panels to display on

## Channel and Dial Management

### get_sub_dial_types()

Get available sub-dial types.

**Returns:** List of available dial types

### get_sub_dial_list(dial_type, page=1)

Get list of sub-dials for a specific type.

**Parameters:**
- `dial_type` (int): Dial type ID
- `page` (int): Page number for pagination

### get_whole_dial_list(page=1)

Get list of complete clock faces.

**Parameters:**
- `page` (int): Page number

**Returns:** List of available clock faces

### select_whole_dial(clock_id)

Select a complete clock face.

**Parameters:**
- `clock_id` (int): Clock face ID

**Example:**
```python
# Get available clock faces
dials = device.get_whole_dial_list()
# Select the first one
device.select_whole_dial(dials[0]['ClockId'])
```

### select_channel_type(channel_type, lcd_independence=None)

Set channel display mode.

**Parameters:**
- `channel_type` (int): 0=whole dial, 1=independent dials
- `lcd_independence` (list, optional): LCD independence settings

### select_sub_dial(clock_id, lcd_index, lcd_independence)

Select a sub-dial for a specific LCD.

**Parameters:**
- `clock_id` (int): Sub-dial ID
- `lcd_index` (int): LCD panel index
- `lcd_independence` (list): Independence settings

## Advanced Features

### command_list(command_list)

Execute multiple commands in sequence.

**Parameters:**
- `command_list` (list): List of command dictionaries

**Example:**
```python
commands = [
    {"Command": "Channel/SetBrightness", "Brightness": 50},
    {"Command": "Channel/OnOffScreen", "OnOff": 1}
]
device.command_list(commands)
```

### url_command_file(command_url)

Execute commands from a URL.

**Parameters:**
- `command_url` (str): URL containing command JSON

### get_font_list()

Get available fonts.

**Returns:** List of font information

**Example:**
```python
fonts = device.get_font_list()
for font in fonts:
    print(f"Font {font['id']}: {font['name']}")
```

## Data Types and Constants

### Display Item Types

| Type | Description |
|------|-------------|
| 6 | Center display item |
| 14 | Top-left corner item |
| 22 | Custom text |
| 23 | Dynamic text with URL update |

### Font IDs

| ID | Description |
|----|-------------|
| 0 | Tiny (5px) |
| 1 | Small (7px) |
| 2 | Medium (10px) |
| 3 | Large (12px) |
| 4 | Extra Large (16px) |

### Color Format

Colors are specified as hex strings: `"#RRGGBB"`

Examples:
- White: `"#FFFFFF"`
- Red: `"#FF0000"`
- Green: `"#00FF00"`
- Blue: `"#0000FF"`

### LCD Panel Indices

The Times Gate has 5 LCD panels, indexed 1-5:
- Panel 1: Top-left
- Panel 2: Top-right
- Panel 3: Center
- Panel 4: Bottom-left
- Panel 5: Bottom-right

## Error Handling

All methods return a dictionary with an `error_code` field:
- `0`: Success
- Non-zero: Error occurred

**Example:**
```python
response = device.set_brightness(50)
if response and response.get('error_code') == 0:
    print("Success!")
else:
    print("Error:", response)
```

## HTTP API Details

All commands are sent as POST requests to:
```
http://{device_ip}:80/post
```

Request format:
```json
{
    "Command": "CommandName",
    "Parameter1": "value1",
    "Parameter2": "value2"
}
```

Response format:
```json
{
    "error_code": 0,
    "result": {...}
}
``` 