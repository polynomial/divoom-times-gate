# Divoom Times Gate API Specification

This document provides the complete API specification for the Divoom Times Gate device, compiled from code analysis and official documentation references.

## API Overview

The Divoom Times Gate communicates via HTTP POST requests to port 80 on the device's IP address. All commands are sent to the `/post` endpoint.

### Base URL
```
http://{device_ip}:80/post
```

### Request Format
All requests use JSON format with a `Command` field and additional parameters:

```json
{
    "Command": "CommandName",
    "Parameter1": "value1",
    "Parameter2": "value2"
}
```

### Response Format
Responses are JSON with an `error_code` field:

```json
{
    "error_code": 0,
    "data": {...}
}
```

Error code 0 indicates success.

---

## Display Control Commands

### Channel/SetBrightness
Set the display brightness.

**Request:**
```json
{
    "Command": "Channel/SetBrightness",
    "Brightness": 50
}
```

**Parameters:**
- `Brightness` (int): 0-100

---

### Channel/OnOffScreen
Turn the display on or off.

**Request:**
```json
{
    "Command": "Channel/OnOffScreen",
    "OnOff": 1
}
```

**Parameters:**
- `OnOff` (int): 1 = on, 0 = off

---

### Channel/GetAllConf
Get all device configuration settings.

**Request:**
```json
{
    "Command": "Channel/GetAllConf"
}
```

**Response:** Returns complete device configuration.

---

### Draw/SendHttpItemList
Send a display list configuration with multiple items.

**Request:**
```json
{
    "Command": "Draw/SendHttpItemList",
    "LcdIndex": 1,
    "NewFlag": 1,
    "BackgroudGif": "http://f.divoom-gz.com/64_64.gif",
    "ItemList": [
        {
            "TextId": 1,
            "type": 22,
            "x": 16,
            "y": 16,
            "dir": 0,
            "font": 2,
            "TextWidth": 48,
            "Textheight": 16,
            "speed": 100,
            "align": 1,
            "TextString": "Hello World",
            "color": "#FFFFFF"
        }
    ]
}
```

**Parameters:**
- `LcdIndex` (int): LCD panel index (1-5)
- `NewFlag` (int): 1 for new display, 0 to update existing
- `BackgroudGif` (string): Background GIF URL
- `ItemList` (array): Array of display items

**Display Item Types:**
- Type 6: Center display item
- Type 14: Date/Time display
- Type 22: Custom text
- Type 23: Dynamic text with URL update

---

### Draw/SendHttpText
Display text on a specific LCD panel.

**Request:**
```json
{
    "Command": "Draw/SendHttpText",
    "LcdIndex": 1,
    "TextId": 1,
    "x": 10,
    "y": 20,
    "dir": 0,
    "font": 3,
    "TextWidth": 48,
    "TextString": "Hello!",
    "speed": 0,
    "color": "#FFFFFF",
    "align": 2
}
```

**Parameters:**
- `LcdIndex` (int): LCD panel (1-5)
- `TextId` (int): Unique text identifier
- `x`, `y` (int): Position (0-63)
- `dir` (int): Direction (0=horizontal, 1=vertical)
- `font` (int): Font size (0-4)
- `TextWidth` (int): Text display width
- `TextString` (string): Text to display
- `speed` (int): Scroll speed (0=static)
- `color` (string): Hex color code
- `align` (int): 1=left, 2=center, 3=right

---

## System Configuration Commands

### Sys/TimeZone
Set the device timezone.

**Request:**
```json
{
    "Command": "Sys/TimeZone",
    "TimeZoneValue": "GMT-8:00"
}
```

---

### Sys/LogAndLat
Set location for weather information.

**Request:**
```json
{
    "Command": "Sys/LogAndLat",
    "Longitude": "-122.4194",
    "Latitude": "37.7749"
}
```

---

### Device/SetUTC
Set system time using UTC timestamp.

**Request:**
```json
{
    "Command": "Device/SetUTC",
    "Utc": 1640995200
}
```

---

### Device/GetDeviceTime
Get current device time.

**Request:**
```json
{
    "Command": "Device/GetDeviceTime"
}
```

---

### Device/SetDisTempMode
Set temperature display mode.

**Request:**
```json
{
    "Command": "Device/SetDisTempMode",
    "Mode": 0
}
```

**Parameters:**
- `Mode` (int): 0 = Celsius, 1 = Fahrenheit

---

### Device/SetMirrorMode
Enable/disable mirror mode.

**Request:**
```json
{
    "Command": "Device/SetMirrorMode",
    "Mode": 1
}
```

---

### Device/SetTime24Flag
Set 12/24 hour time format.

**Request:**
```json
{
    "Command": "Device/SetTime24Flag",
    "Mode": 1
}
```

**Parameters:**
- `Mode` (int): 1 = 24-hour, 0 = 12-hour

---

### Device/GetWeatherInfo
Get current weather information.

**Request:**
```json
{
    "Command": "Device/GetWeatherInfo"
}
```

---

## Tools and Utilities

### Tools/SetTimer
Control countdown timer.

**Request:**
```json
{
    "Command": "Tools/SetTimer",
    "Minute": 5,
    "Second": 0,
    "Status": 1
}
```

**Parameters:**
- `Minute` (int): Minutes (0-99)
- `Second` (int): Seconds (0-59)
- `Status` (int): 1 = start, 0 = stop

---

### Tools/SetStopWatch
Control stopwatch.

**Request:**
```json
{
    "Command": "Tools/SetStopWatch",
    "Status": 1
}
```

**Parameters:**
- `Status` (int): 1 = start, 2 = stop, 3 = reset

---

### Tools/SetScoreBoard
Display scoreboard.

**Request:**
```json
{
    "Command": "Tools/SetScoreBoard",
    "BlueScore": 10,
    "RedScore": 8
}
```

---

### Tools/SetNoiseStatus
Control noise meter.

**Request:**
```json
{
    "Command": "Tools/SetNoiseStatus",
    "NoiseStatus": 1
}
```

---

### Device/PlayBuzzer
Play buzzer sound.

**Request:**
```json
{
    "Command": "Device/PlayBuzzer",
    "ActiveTimeInCycle": 100,
    "OffTimeInCycle": 100,
    "PlayTotalTime": 300
}
```

---

## Animation and Graphics

### Device/PlayGif
Play GIF animations on LCD panels.

**Request:**
```json
{
    "Command": "Device/PlayGif",
    "FileName": ["anim1.gif", "anim2.gif"],
    "LcdArray": [1, 2]
}
```

---

### Device/PlayGifLCDs
Play different GIFs on each LCD.

**Request:**
```json
{
    "Command": "Device/PlayGifLCDs",
    "LCD0GifFile": "lcd1.gif",
    "LCD1GifFile": "lcd2.gif",
    "LCD2GifFile": "lcd3.gif",
    "LCD3GifFile": "lcd4.gif",
    "LCD4GifFile": "lcd5.gif"
}
```

---

### Draw/SendRemote
Play GIF from Divoom server.

**Request:**
```json
{
    "Command": "Draw/SendRemote",
    "FileId": "12345",
    "LcdArray": [1, 2, 3]
}
```

---

### Draw/SendHttpGif
Send custom animation frames.

**Request:**
```json
{
    "Command": "Draw/SendHttpGif",
    "PicNum": 10,
    "PicWidth": 64,
    "PicOffset": 0,
    "PicID": 1,
    "PicSpeed": 100,
    "PicData": "base64_encoded_data",
    "LcdArray": [1]
}
```

---

## Channel and Dial Management

### Channel/GetDialType
Get available sub-dial types.

**Request:**
```json
{
    "Command": "Channel/GetDialType"
}
```

---

### Channel/GetDialList
Get list of sub-dials.

**Request:**
```json
{
    "Command": "Channel/GetDialList",
    "DialType": 1,
    "Page": 1
}
```

---

### Channel/Get5LcdClockListForCommon
Get whole dial list.

**Request:**
```json
{
    "Command": "Channel/Get5LcdClockListForCommon",
    "Page": 1
}
```

---

### Channel/Set5LcdWholeClockId
Select a whole dial.

**Request:**
```json
{
    "Command": "Channel/Set5LcdWholeClockId",
    "ClockId": 100
}
```

---

### Channel/Set5LcdChannelType
Set channel display mode.

**Request:**
```json
{
    "Command": "Channel/Set5LcdChannelType",
    "ChannelType": 0,
    "LcdIndependence": [1, 1, 1, 1, 1]
}
```

**Parameters:**
- `ChannelType` (int): 0 = whole dial, 1 = independent dials

---

### Channel/Get5LcdInfoV2
Get channel information.

**Request:**
```json
{
    "Command": "Channel/Get5LcdInfoV2",
    "DeviceId": "device_id",
    "DeviceType": "LCD"
}
```

---

### Channel/SetClockSelectId
Select sub-dial for LCD.

**Request:**
```json
{
    "Command": "Channel/SetClockSelectId",
    "ClockId": 50,
    "LcdIndex": 1,
    "LcdIndependence": [1, 0, 0, 0, 0]
}
```

---

### Channel/SetEqPosition
Select visualizer channel.

**Request:**
```json
{
    "Command": "Channel/SetEqPosition",
    "EqPosition": 1,
    "LcdIndex": 3,
    "LcdIndependence": [0, 0, 1, 0, 0]
}
```

---

## Advanced Features

### Draw/CommandList
Execute multiple commands.

**Request:**
```json
{
    "Command": "Draw/CommandList",
    "CommandList": [
        {"Command": "Channel/SetBrightness", "Brightness": 50},
        {"Command": "Channel/OnOffScreen", "OnOff": 1}
    ]
}
```

---

### Draw/UseHTTPCommandSource
Execute commands from URL.

**Request:**
```json
{
    "Command": "Draw/UseHTTPCommandSource",
    "CommandUrl": "http://example.com/commands.json"
}
```

---

### Device/GetTimeDialFontList
Get available fonts.

**Request:**
```json
{
    "Command": "Device/GetTimeDialFontList"
}
```

---

### Device/GetImgLikeList
Get liked images list.

**Request:**
```json
{
    "Command": "Device/GetImgLikeList",
    "DeviceId": "device_id",
    "DeviceMac": "device_mac",
    "Page": 1
}
```

---

### Device/GetImgUploadList
Get uploaded images list.

**Request:**
```json
{
    "Command": "Device/GetImgUploadList",
    "DeviceId": "device_id",
    "DeviceMac": "device_mac",
    "Page": 1
}
```

---

## Data Types Reference

### Font IDs
- 0: Tiny (5px)
- 1: Small (7px)
- 2: Medium (10px)
- 3: Large (12px)
- 4: Extra Large (16px)

### LCD Panel Indices
```
[1] [2]
  [3]
[4] [5]
```

- Panel 1: Top-left
- Panel 2: Top-right
- Panel 3: Center
- Panel 4: Bottom-left
- Panel 5: Bottom-right

### Color Format
Colors use hex format: `#RRGGBB`

Examples:
- White: `#FFFFFF`
- Red: `#FF0000`
- Green: `#00FF00`
- Blue: `#0000FF`
- Yellow: `#FFFF00`
- Cyan: `#00FFFF`
- Magenta: `#FF00FF`

### Display Item Types
- Type 6: Center display item
- Type 14: Top-left corner item (date/time)
- Type 22: Custom text
- Type 23: Dynamic text with URL update

### External API Endpoints

The device can fetch data from external URLs:

- Date/Time API: `http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0`
  - Returns: `{"ReturnCode":0,"ReturnMessage":"","DispData":"2025-03-22 06:10:58"}`

- Default Background GIF: `http://f.divoom-gz.com/64_64.gif`

---

## Error Codes

- `0`: Success
- Non-zero: Error occurred (specific codes vary by command)

---

## Usage Examples

### Display Custom Message

```python
# Python example
import requests

device_ip = "192.168.1.100"
url = f"http://{device_ip}:80/post"

# Display "Hello World" on center panel
data = {
    "Command": "Draw/SendHttpText",
    "LcdIndex": 3,
    "TextId": 1,
    "x": 32,
    "y": 32,
    "dir": 0,
    "font": 3,
    "TextWidth": 64,
    "TextString": "Hello World!",
    "speed": 0,
    "color": "#00FF00",
    "align": 2
}

response = requests.post(url, json=data)
print(response.json())
```

### Set Brightness and Turn On

```bash
# Using curl
curl -X POST http://192.168.1.100:80/post \
  -H "Content-Type: application/json" \
  -d '{
    "Command": "Channel/SetBrightness",
    "Brightness": 75
  }'

curl -X POST http://192.168.1.100:80/post \
  -H "Content-Type: application/json" \
  -d '{
    "Command": "Channel/OnOffScreen",
    "OnOff": 1
  }'
```

---

This documentation represents the complete API specification for the Divoom Times Gate device, compiled from code analysis and implementation details. 