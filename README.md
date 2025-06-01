# Divoom Times Gate Python Library

A comprehensive Python library for controlling Divoom Times Gate devices via HTTP API.

## Features

- ✨ **Complete API Coverage** - Access all Times Gate functionality
- 🔄 **Modern Async/Await** - Built on asyncio and aiohttp
- 🎛️ **Individual Panel Control** - Manage each of the 5 LCD panels independently  
- 🛠️ **Command Line Tools** - Control your device from the terminal
- 🌐 **Device Discovery** - Find Times Gate devices on your network
- 📦 **Display Lists** - Complex custom layouts (like the original display.py)
- 📝 **Text Display** - Multiple fonts and alignments  
- ⏱️ **Built-in Tools** - Countdown, stopwatch, scoreboard
- 🌡️ **Weather & Temperature** - Location-based weather display
- 🎨 **GIF Animations** - Display animated content
- 📡 **Raw Commands** - Access undocumented features

## Important Note: Text Display Limitations

**Currently, custom text display is not working via the HTTP API.** While the device accepts text commands without errors, text does not appear on the display. This appears to require enabling a specific mode or app via the Divoom mobile app. All other features (timers, scoreboards, weather, brightness, etc.) work correctly.

## Installation

```bash
pip install divoom-timesgate
```

For development with nix-shell:
```bash
nix-shell
pip install -e .
```

## Quick Start

```python
import asyncio
from divoom_timesgate import TimesGateDevice

async def main():
    # Connect to your Times Gate device
    async with TimesGateDevice("192.168.1.100") as device:
        # Set brightness
        await device.set_brightness(50)
        
        # Display custom text
        await device.create_text_display(
            text="Hello World!",
            panel=1,
            color="#00FF00"
        )
        
        # Create multi-item display (like old display.py)
        from divoom_timesgate import TextDisplayItem, DateTimeDisplayItem
        
        items = [
            TextDisplayItem(1, "Divoom Times Gate", x=0, y=10, color="#FF0000"),
            DateTimeDisplayItem(2, x=0, y=48)
        ]
        await device.create_multi_item_display(items)
        
        # Show countdown timer on panel 3
        await device.set_panel_timer(panel=3, minutes=5, seconds=0)

asyncio.run(main())
```

## Panel Layout

The Times Gate has 5 LCD panels arranged horizontally:

```
[1] [2] [3] [4] [5]
```

You can display different content on each panel!

## Command Line Tools

Control your device from the terminal:

```bash
# Set brightness
divoom-brightness 75

# Set weather location
divoom-weather --city "new york"

# Control display
divoom-screen on
divoom-screen off

# Full CLI with all commands
divoom --help
```

## Panel-Specific Features (New Discovery!)

We've discovered undocumented panel-specific control:

```python
# Different timers on each panel
await device.set_panel_timer(panel=1, minutes=1, seconds=0)
await device.set_panel_timer(panel=2, minutes=2, seconds=0)

# Different scores on each panel
await device.set_panel_scoreboard(panel=1, red_score=10, blue_score=5)
await device.set_panel_scoreboard(panel=2, red_score=3, blue_score=2)
```

See [examples/multi_panel_demo.py](examples/multi_panel_demo.py) for interactive demos!

## API Documentation

- [Python API Reference](docs/API.md)
- [HTTP API Reference](docs/API_REFERENCE.md)
- [Panel Control Guide](docs/PANEL_CONTROL.md)
- [Examples](examples/)

## Working Features

✅ **System Control**
- Brightness adjustment
- Screen on/off
- Temperature unit (°C/°F)
- Time format (12/24 hour)
- Device reboot

✅ **Display Tools**
- Countdown timers (global and per-panel)
- Stopwatch
- Scoreboard (global and per-panel)
- Noise meter control

✅ **Configuration**
- Weather location
- Time zone
- Mirror mode

❌ **Not Working**
- Custom text display (requires mobile app configuration)
- Individual panel channel switching
- GIF animations

## Examples

Check out the [examples](examples/) directory for more:
- `multi_panel_demo.py` - Interactive demos showing panel-specific control
- `quick_demo.py` - Basic functionality demo
- `weather_dashboard.py` - Weather-focused display
- `game_scoreboard.py` - Sports score tracker

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to Divoom for creating these interesting devices
- API documentation from [https://docin.divoom-gz.com/](https://docin.divoom-gz.com/)

## Support

If you encounter any issues or have questions:
1. Check the [troubleshooting guide](docs/TROUBLESHOOTING.md)
2. Look at existing [issues](https://github.com/yourusername/divoom-times-gate/issues)
3. Create a new issue with details about your problem 