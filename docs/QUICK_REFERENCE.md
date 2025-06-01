# Divoom Times Gate Quick Reference

## Environment Setup

```bash
# Set device IP address
export DIVOOM_TIMES_GATE_IP=192.168.1.100
```

## Command Line Tools

### Using the Main CLI (`divoom`)

```bash
# Screen control
divoom screen on
divoom screen off

# Brightness
divoom brightness 50        # Set to 50%
divoom brightness --cycle   # Cycle through levels

# Clock settings
divoom clock --24h          # 24-hour format
divoom clock --12h          # 12-hour format
divoom clock --timezone "GMT-8:00"
divoom clock --sync         # Sync with system time

# Weather
divoom weather --location 37.7749 -122.4194  # Set location
divoom weather --celsius    # Use Celsius
divoom weather --fahrenheit # Use Fahrenheit
divoom weather --show       # Display current weather

# Timer & Stopwatch
divoom timer 5              # 5-minute timer
divoom timer 10 30          # 10 minutes 30 seconds
divoom timer --stop         # Stop timer
divoom stopwatch start
divoom stopwatch stop
divoom stopwatch reset

# Scoreboard
divoom scoreboard 10 8      # Blue: 10, Red: 8

# Device settings
divoom settings             # View all settings
divoom settings --json      # JSON output

# Buzzer
divoom buzzer               # Default beep
divoom buzzer --pattern long
```

### Individual Tool Scripts

```bash
# Display control
divoom-display --text "Hello World!" --text-color "#00FF00"

# Brightness control
divoom-brightness          # Cycle through levels
divoom-brightness 75       # Set to 75%

# Weather display
divoom-weather
divoom-weather --set-location 37.7749 -122.4194

# Screen power
divoom-screen on
divoom-screen off
```

## Python API Quick Examples

### Basic Setup

```python
from src.divoom_times_gate import DivoomTimesGate

device = DivoomTimesGate()
```

### Common Operations

```python
# Screen & Brightness
device.switch_screen(1)     # On
device.switch_screen(0)     # Off
device.set_brightness(50)   # 50%

# Display text
device.send_text(
    lcd_index=1,
    text_id=1,
    x=10, y=20,
    dir=0,
    font=3,
    text_width=48,
    text_string="Hello!",
    speed=0,
    color="#FFFFFF",
    align=2  # Center
)

# Timer & Stopwatch
device.set_countdown_tool(5, 0, 1)    # 5-minute timer
device.set_stopwatch_tool(1)          # Start
device.set_stopwatch_tool(2)          # Stop
device.set_stopwatch_tool(3)          # Reset

# Scoreboard
device.set_scoreboard_tool(10, 8)     # Blue: 10, Red: 8

# Weather
device.set_weather_location(-122.4194, 37.7749)
weather = device.get_weather()

# Play sound
device.play_buzzer(100, 100, 300)    # Beep pattern
```

### Display List Example

```python
items = [
    {
        "TextId": 1,
        "type": 22,  # Custom text
        "x": 32, "y": 20,
        "font": 3,
        "TextWidth": 64,
        "TextString": "Welcome!",
        "color": "#00FF00",
        "align": 2
    }
]

device.send_display_list(
    lcd_index=3,  # Center panel
    new_flag=1,
    background_gif="",
    item_list=items
)
```

## Display Item Types

| Type | Description | Key Parameters |
|------|-------------|----------------|
| 6 | Center display | Standard positioning |
| 14 | Date/Time display | Auto-updates |
| 22 | Custom text | TextString required |
| 23 | Dynamic text (URL) | TextString = URL, update_time |

## Font Sizes

| ID | Size | Description |
|----|------|-------------|
| 0 | 5px | Tiny |
| 1 | 7px | Small |
| 2 | 10px | Medium |
| 3 | 12px | Large |
| 4 | 16px | Extra Large |

## LCD Panel Layout

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

## Color Examples

- White: `#FFFFFF`
- Red: `#FF0000`
- Green: `#00FF00`
- Blue: `#0000FF`
- Yellow: `#FFFF00`
- Cyan: `#00FFFF`
- Magenta: `#FF00FF`
- Orange: `#FFA500`

## Troubleshooting

```bash
# Test connection
ping $DIVOOM_TIMES_GATE_IP

# Check settings
divoom settings

# Send raw command
divoom raw "Channel/GetAllConf" --data '{}'
```

## Example Scripts

See `docs/examples/` for complete examples:
- `custom_clock.py` - Custom clock display
- `notification_system.py` - Notification system
- `weather_dashboard.py` - Weather display
- `game_scoreboard.py` - Interactive scoreboard 