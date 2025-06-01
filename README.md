# Divoom Times Gate Controller

A comprehensive Python and PHP library for controlling Divoom Times Gate devices, with complete API documentation and command-line tools.

## 📖 Documentation

Complete documentation is available in the [docs/](docs/) directory:

- **[API Reference](docs/API_REFERENCE.md)** - Complete HTTP API documentation
- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running quickly
- **[Python Library Documentation](docs/API.md)** - Python API reference
- **[Examples](docs/examples/)** - Working code examples

## 🚀 Quick Start

### Installation

#### From PyPI (when published)
```bash
pip install divoom-timesgate
```

#### From Source
```bash
# Clone the repository
git clone https://github.com/divoom-timesgate/divoom-times-gate.git
cd divoom-times-gate

# Install in development mode
pip install -e .

# Or just install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### Python Library
```python
from divoom_timesgate import TimesGateDevice

# Connect to device
device = TimesGateDevice("192.168.68.50")

# Control brightness
await device.set_brightness(75)

# Display text
await device.send_text("Hello World", color="#FF0000")

# Play GIF
await device.play_gif("http://example.com/animation.gif")
```

#### Command Line
```bash
# Set brightness
./bin/divoom brightness 75

# Display text
./bin/divoom text "Hello World" --color "#FF0000"

# Show weather
./bin/divoom weather --city "New York"
```

#### Direct HTTP API
```bash
curl -X POST http://192.168.68.50:80/post \
  -H "Content-Type: application/json" \
  -d '{"Command":"Channel/SetBrightness","Brightness":75}'
```

## 🔧 Language Bindings

### [Python Library](divoom_timesgate/)
Full-featured async Python library with comprehensive API coverage:
- Device discovery
- System settings control
- Display management
- Animation and text display
- Tools (timer, stopwatch, scoreboard, etc.)

### [PHP Library](php-divoom-timesgate/)
PHP library for web applications (see directory for documentation)

## 📦 Repository Structure

```
divoom-times-gate/
├── divoom_timesgate/       # Python library
│   ├── device.py          # Main device control class
│   ├── discovery.py       # Device discovery
│   ├── models.py          # Data models and enums
│   └── exceptions.py      # Error handling
├── php-divoom-timesgate/   # PHP library
├── bin/                    # Command-line tools
│   ├── divoom             # Main CLI tool
│   ├── divoom-brightness  # Brightness control
│   ├── divoom-screen      # Screen control
│   ├── divoom-display     # Display images/text
│   └── divoom-weather     # Weather display
├── docs/                   # Complete documentation
│   ├── API_REFERENCE.md   # HTTP API reference
│   ├── API.md            # Python API reference
│   └── examples/         # Code examples
└── scripts/               # Utility scripts
```

## ⚡ Features

- **Complete API Coverage**: All Times Gate HTTP API endpoints
- **Multiple Interfaces**: Python library, PHP library, CLI tools, direct HTTP
- **Async Support**: Modern async/await Python implementation
- **Type Safety**: Full type hints and enums
- **Device Discovery**: Automatic device detection on local network
- **Comprehensive Documentation**: Detailed API reference and examples

## 📡 Device Information

The Divoom Times Gate has 5 LCD panels arranged in a cross pattern:

```
     [2]
  [1][5][3]
  [4]
```

Each panel can be controlled independently or as a group.

## 🛠️ Development

### Running Tests
```bash
# Test brightness control
python tests/test_brightness_simple.py

# Test async version
python tests/test_brightness.py
```

### Building the Package
```bash
# Install build tools
pip install build

# Build the package
python -m build
```

### Publishing to PyPI
```bash
# Install twine
pip install twine

# Upload to PyPI
python -m twine upload dist/*
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Divoom for creating the Times Gate device
- API documentation from https://docin.divoom-gz.com/
- Contributors to the Python and PHP implementations

## 📧 Contact

For device-specific questions: developer@divoom.com 