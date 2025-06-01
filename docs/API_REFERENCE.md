# Divoom Times Gate API Reference

This is the complete API reference for the Divoom Times Gate device. All commands are sent via HTTP POST to `http://{device_ip}:80/post`.

## Table of Contents

- [System Settings](#system-settings)
- [Display Control](#display-control)
- [Animation & Text](#animation--text)
- [Tools](#tools)
- [Advanced Features](#advanced-features)
- [Common Issues](#common-issues)

---

## System Settings

### Set Brightness

Control the display brightness (0-100).

```json
{
    "Command": "Channel/SetBrightness",
    "Brightness": 75
}
```

**Parameters:**
- `Brightness` (number): Value from 0 to 100

**Response:**
```json
{
    "error_code": 0
}
```

### Get All Settings

Retrieve all device settings.

```json
{
    "Command": "Channel/GetAllConf"
}
```

**Response:**
```json
{
    "error_code": 0,
    "Brightness": 80,
    "RotationFlag": 0,
    "ClockTime": 60,
    "GalleryTime": 60,
    "SingleGalleyTime": 5,
    "PowerOnChannelId": 1,
    "GalleryShowTimeFlag": 1,
    "CurClockId": 217,
    "Time24Flag": 1,
    "TemperatureMode": 1,
    "GalleryFlag": 1,
    "GyroFlag": 1,
    "MirrorFlag": 0,
    "LightSwitch": 1
}
```

### Set Device Time

Set the device's current time.

```json
{
    "Command": "Device/SetUTC",
    "Utc": 1672531200
}
```

**Parameters:**
- `Utc` (number): Unix timestamp

### Get Device Time

Get the device's current time.

```json
{
    "Command": "Device/GetDeviceTime"
}
```

**Response:**
```json
{
    "error_code": 0,
    "UTCTime": 1672531200,
    "LocalTime": "2023-01-01 12:00:00"
}
```

### Set Time Zone

Configure the device time zone.

```json
{
    "Command": "Sys/TimeZone",
    "TimeZoneValue": "GMT-5"
}
```

**Parameters:**
- `TimeZoneValue` (string): Time zone string (e.g., "GMT-5", "GMT+8")

### Set Temperature Mode

Switch between Celsius and Fahrenheit.

```json
{
    "Command": "Device/SetDisTempMode",
    "Mode": 0
}
```

**Parameters:**
- `Mode` (number): 0 = Celsius, 1 = Fahrenheit

### Set Mirror Mode

Enable or disable display mirroring.

```json
{
    "Command": "Device/SetMirrorMode",
    "Mode": 0
}
```

**Parameters:**
- `Mode` (number): 0 = Off, 1 = On

### Set Hour Mode

Switch between 12-hour and 24-hour time format.

```json
{
    "Command": "Device/SetTime24Flag",
    "Mode": 1
}
```

**Parameters:**
- `Mode` (number): 0 = 12-hour, 1 = 24-hour

### Screen Switch

Turn the display on or off.

```json
{
    "Command": "Channel/OnOffScreen",
    "OnOff": 1
}
```

**Parameters:**
- `OnOff` (number): 0 = Off, 1 = On

### Weather Area Setting

Set the location for weather display.

```json
{
    "Command": "Sys/LogAndLat",
    "Longitude": "-73.935242",
    "Latitude": "40.730610"
}
```

**Parameters:**
- `Longitude` (string): Longitude coordinate
- `Latitude` (string): Latitude coordinate

### System Reboot

Reboot the device.

```json
{
    "Command": "Device/Reboot"
}
```

---

## Display Control

### Select Channel Type

Choose between whole dial or individual LCD control.

```json
{
    "Command": "Channel/GetCurChannelInfo"
}
```

**Response:**
```json
{
    "error_code": 0,
    "ChannelType": 0,
    "ClockId": 217,
    "LcdIndependence": 978
}
```

### Select Whole Dial

Select a clock face for all displays.

```json
{
    "Command": "Channel/SetWholeDial",
    "ClockId": 61
}
```

**Parameters:**
- `ClockId` (number): ID of the clock face

### Select Individual Dial

Control individual LCD panels.

```json
{
    "Command": "Channel/SetIndividualDial",
    "LcdId": 1,
    "ClockId": 61
}
```

**Parameters:**
- `LcdId` (number): LCD panel index (1-5)
- `ClockId` (number): Clock face ID

### Get Dial List

Get available clock faces.

```json
{
    "Command": "Channel/GetWholeDial"
}
```

**Response:**
```json
{
    "error_code": 0,
    "ClockList": [
        {
            "ClockId": 61,
            "Name": "Digital Clock"
        },
        {
            "ClockId": 182,
            "Name": "Analog Clock"
        }
    ]
}
```

### LCD Panel Layout

The Times Gate has 5 LCD panels arranged in a cross pattern:

```
     [2]
  [1][5][3]
     [4]
```

- Panel 1: Left
- Panel 2: Top
- Panel 3: Right
- Panel 4: Bottom
- Panel 5: Center

---

## Animation & Text

### Send Text

Display scrolling or static text.

```json
{
    "Command": "Draw/SendHttpText",
    "TextId": 1,
    "x": 0,
    "y": 0,
    "dir": 0,
    "font": 2,
    "TextWidth": 64,
    "TextString": "Hello World",
    "speed": 100,
    "color": "#FF0000",
    "align": 1
}
```

**Parameters:**
- `TextId` (number): Unique text ID (0-19)
- `x` (number): X position
- `y` (number): Y position
- `dir` (number): Direction (0=left, 1=right)
- `font` (number): Font ID (0-4)
- `TextWidth` (number): Text area width
- `TextString` (string): Text to display
- `speed` (number): Scroll speed (0-100)
- `color` (string): Hex color (#RRGGBB)
- `align` (number): Alignment (0=left, 1=center, 2=right)

### Clear Text

Clear displayed text.

```json
{
    "Command": "Draw/ClearHttpText",
    "TextId": 1
}
```

**Parameters:**
- `TextId` (number): Text ID to clear (-1 for all)

### Play GIF

Play a GIF animation from URL.

```json
{
    "Command": "Device/PlayTFGif",
    "FileType": 2,
    "FileName": "http://example.com/animation.gif"
}
```

**Parameters:**
- `FileType` (number): 1 = Local file, 2 = URL
- `FileName` (string): File path or URL

### Send Animation

Send custom frame animation.

```json
{
    "Command": "Draw/SendHttpGif",
    "PicNum": 2,
    "PicWidth": 64,
    "PicOffset": 0,
    "PicID": 1,
    "PicSpeed": 100,
    "PicData": "base64_encoded_frame_data"
}
```

**Parameters:**
- `PicNum` (number): Total number of frames
- `PicWidth` (number): Frame width
- `PicOffset` (number): Current frame index
- `PicID` (number): Animation ID
- `PicSpeed` (number): Frame duration in ms
- `PicData` (string): Base64 encoded RGB565 frame data

### Get Font List

Get available fonts.

```json
{
    "Command": "Device/GetFontList"
}
```

**Response:**
```json
{
    "error_code": 0,
    "FontList": [
        {"id": 0, "name": "5px", "height": 5},
        {"id": 1, "name": "8px", "height": 8},
        {"id": 2, "name": "11px", "height": 11},
        {"id": 3, "name": "14px", "height": 14},
        {"id": 4, "name": "16px", "height": 16}
    ]
}
```

### Send Display List

Send multiple display items.

```json
{
    "Command": "Draw/SendHttpList",
    "ItemList": [
        {
            "TextId": 6,
            "type": 6,
            "x": 0,
            "y": 0,
            "color": "#FFFFFF",
            "font": 2,
            "align": 1
        },
        {
            "TextId": 14,
            "type": 14,
            "x": 0,
            "y": 16,
            "color": "#00FF00",
            "font": 1,
            "string": "2023-12-31"
        },
        {
            "TextId": 22,
            "type": 22,
            "x": 0,
            "y": 32,
            "color": "#FF0000",
            "font": 2,
            "string": "Custom Text"
        }
    ]
}
```

**Display Types:**
- `6`: Center display
- `14`: Date/time
- `22`: Custom text
- `23`: Dynamic URL text

---

## Tools

### Countdown Timer

Set a countdown timer.

```json
{
    "Command": "Tools/SetTimer",
    "Minute": 5,
    "Second": 30,
    "Status": 1
}
```

**Parameters:**
- `Minute` (number): Minutes (0-99)
- `Second` (number): Seconds (0-59)
- `Status` (number): 0 = Stop, 1 = Start

### Stopwatch

Control the stopwatch.

```json
{
    "Command": "Tools/SetStopWatch",
    "Status": 1
}
```

**Parameters:**
- `Status` (number): 0 = Stop/Reset, 1 = Start

### Scoreboard

Display a scoreboard.

```json
{
    "Command": "Tools/SetScoreBoard",
    "RedScore": 12,
    "BlueScore": 8
}
```

**Parameters:**
- `RedScore` (number): Red team score (0-999)
- `BlueScore` (number): Blue team score (0-999)

### Noise Meter

Activate noise level display.

```json
{
    "Command": "Tools/SetNoiseStatus",
    "Status": 1
}
```

**Parameters:**
- `Status` (number): 0 = Off, 1 = On

### Play Buzzer

Sound the buzzer.

```json
{
    "Command": "Device/PlayBuzzer",
    "ActiveTimeInCycle": 500,
    "OffTimeInCycle": 500,
    "PlayTotalTime": 2000
}
```

**Parameters:**
- `ActiveTimeInCycle` (number): Buzzer on time in ms
- `OffTimeInCycle` (number): Buzzer off time in ms
- `PlayTotalTime` (number): Total duration in ms

---

## Advanced Features

### Command List

Execute multiple commands in sequence.

```json
{
    "Command": "Draw/CommandList",
    "CommandList": [
        {
            "Command": "Channel/SetBrightness",
            "Brightness": 100
        },
        {
            "Command": "Device/PlayBuzzer",
            "ActiveTimeInCycle": 100,
            "OffTimeInCycle": 100,
            "PlayTotalTime": 500
        }
    ]
}
```

### URL Command File

Execute commands from a URL.

```json
{
    "Command": "Draw/SendRemote",
    "CommandUrl": "http://example.com/commands.json"
}
```

The URL should return a JSON array of commands.

---

## Common Issues

### Error Codes

- `0`: Success
- `1`: Invalid command
- `2`: Invalid parameters
- `3`: Device busy
- `4`: Network error

### Troubleshooting

1. **Connection Issues**
   - Ensure device is on the same network
   - Check IP address is correct
   - Verify port 80 is accessible

2. **Command Not Working**
   - Check JSON syntax
   - Verify command name spelling
   - Ensure all required parameters are included

3. **Display Issues**
   - Check brightness is not 0
   - Verify screen is turned on
   - Ensure content fits within display bounds

### Best Practices

1. **Rate Limiting**: Wait at least 100ms between commands
2. **Animation**: Use PicID to manage multiple animations
3. **Text**: TextId 0-19 are available for simultaneous text
4. **Batching**: Use CommandList for atomic operations

---

*Documentation source: [https://docin.divoom-gz.com/](https://docin.divoom-gz.com/)* 