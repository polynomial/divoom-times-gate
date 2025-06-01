# Panel-Specific Control

The Divoom Times Gate has 5 LCD panels arranged horizontally. While the official documentation doesn't clearly describe this, we've discovered that you can control individual panels using the `LcdId` parameter.

## Panel Layout

The 5 panels are arranged horizontally:
```
[1] [2] [3] [4] [5]
```

## Current Channel Configuration

You can check which channel each panel is displaying:

```python
result = await device.send_raw_command({"Command": "Channel/GetIndex"})
channels = result.get('SelectIndex', [])
# Returns array like [2, 0, 0, 2, 0]
# where 0 = clock/normal, 2 = VU meter/sound analyzer
```

## Panel-Specific Commands

### Timers on Specific Panels

```python
# Display a 1:30 timer on panel 2
await device.send_raw_command({
    "Command": "Tools/SetTimer",
    "Minute": 1,
    "Second": 30,
    "Status": 1,  # 1 = start, 0 = stop
    "LcdId": 2    # Panel number (1-5)
})
```

### Scoreboards on Specific Panels

```python
# Display scoreboard on panel 3
await device.send_raw_command({
    "Command": "Tools/SetScoreBoard",
    "RedScore": 42,
    "BlueScore": 17,
    "LcdId": 3    # Panel number (1-5)
})
```

## Example: Different Content on Each Panel

```python
import asyncio
from divoom_timesgate import TimesGateDevice

async def multi_panel_demo():
    async with TimesGateDevice("192.168.68.50") as device:
        # Turn off noise meters
        await device.set_noise_meter(False)
        
        # Set different timers on each panel
        timers = [
            {"panel": 1, "time": "0:10"},
            {"panel": 2, "time": "0:20"},
            {"panel": 3, "time": "0:30"},
            {"panel": 4, "time": "0:40"},
            {"panel": 5, "time": "0:50"},
        ]
        
        for timer in timers:
            await device.send_raw_command({
                "Command": "Tools/SetTimer",
                "Minute": 0,
                "Second": int(timer["time"].split(":")[1]),
                "Status": 1,
                "LcdId": timer["panel"]
            })
            
asyncio.run(multi_panel_demo())
```

## Notes

- The `LcdId` parameter is not documented in the official API docs but works with tool commands
- Text display (`Draw/SendHttpText`) still doesn't work even with `LcdId` - this appears to require a specific mode/app
- Individual panel channel switching (`Channel/SetIndividualDial`) doesn't work as documented

## What Works vs What Doesn't

### ✅ Works with LcdId:
- `Tools/SetTimer` - Countdown timers
- `Tools/SetScoreBoard` - Scoreboards
- `Channel/SetIndex` with array - Can change all panel channels at once

### ❌ Doesn't Work:
- `Channel/SetIndividualDial` - Returns "illegal json" error
- `Draw/SendHttpText` with `LcdId` - Text still doesn't display
- Individual panel channel switching

This discovery enables creating interesting multi-panel displays using timers and scoreboards! 