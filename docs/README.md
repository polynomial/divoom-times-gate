# Divoom Times Gate Documentation

Welcome to the comprehensive documentation for the Divoom Times Gate device. This documentation provides complete API reference, language bindings, and examples.

## 📚 Documentation Structure

### [API Reference](API_REFERENCE.md)
Complete API documentation for all Times Gate commands, organized by category:
- **[System Settings](API_REFERENCE.md#system-settings)** - Brightness, time, weather, display settings
- **[Display Control](API_REFERENCE.md#display-control)** - LCD panels, dial control, channel selection
- **[Animation & Text](API_REFERENCE.md#animation--text)** - GIF playback, text display, custom animations
- **[Tools](API_REFERENCE.md#tools)** - Timer, stopwatch, scoreboard, noise meter, buzzer
- **[Advanced Features](API_REFERENCE.md#advanced-features)** - Command batching, URL commands

### [Quick Start Guide](QUICK_START.md)
Get up and running quickly with:
- Device discovery
- Basic commands
- Common use cases
- Troubleshooting

### [Examples](EXAMPLES.md)
Practical examples for common tasks:
- Clock customization
- Weather display
- Notification system
- Animation creation
- Game scoreboard

## 🔧 Language Bindings

### [Python Library](../divoom_timesgate/)
Full-featured Python library with async support:
```python
from divoom_timesgate import TimesGateDevice

device = TimesGateDevice("192.168.68.50")
await device.set_brightness(75)
```

### [PHP Library](../php-divoom-timesgate/)
PHP library for web applications:
```php
use Divoom\TimesGate\TimesGateDevice;

$device = new TimesGateDevice("192.168.68.50");
$device->setBrightness(75);
```

## 📡 API Basics

All Times Gate commands use HTTP POST requests to `http://{device_ip}:80/post` with JSON payloads:

```json
{
    "Command": "Channel/SetBrightness",
    "Brightness": 75
}
```

## 🚀 Quick Examples

### Set Brightness
```bash
curl -X POST http://192.168.68.50:80/post \
  -H "Content-Type: application/json" \
  -d '{"Command":"Channel/SetBrightness","Brightness":75}'
```

### Display Text
```bash
curl -X POST http://192.168.68.50:80/post \
  -H "Content-Type: application/json" \
  -d '{"Command":"Draw/SendHttpText","TextId":1,"x":0,"y":0,"dir":0,"font":2,"TextWidth":64,"TextString":"Hello World","speed":100,"color":"#FF0000"}'
```

## 📖 Additional Resources

- [Command Line Tools](TOOLS.md) - CLI utilities for Times Gate control
- [Changelog](CHANGELOG.md) - Version history and updates
- [Contributing](CONTRIBUTING.md) - How to contribute to this project

## 🔍 Device Discovery

Find Times Gate devices on your network:

```python
# Python
from divoom_timesgate import discover_devices
devices = await discover_devices()

# PHP
use Divoom\TimesGate\Discovery;
$devices = Discovery::findDevices();
```

## ⚡ Need Help?

- Check the [Troubleshooting Guide](QUICK_START.md#troubleshooting)
- Review [Common Issues](API_REFERENCE.md#common-issues)
- Contact: developer@divoom.com 