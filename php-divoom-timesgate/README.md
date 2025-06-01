# Divoom Times Gate PHP Library

A PHP library for controlling Divoom Times Gate devices via their HTTP API.

## Installation

```bash
composer require divoom/timesgate
```

## Quick Start

```php
<?php
require_once 'vendor/autoload.php';

use Divoom\TimesGate\TimesGateDevice;

// Create device instance
$device = new TimesGateDevice('192.168.68.50');

// Set brightness
$device->setBrightness(75);

// Display text
$device->sendText('Hello World', [
    'color' => '#FF0000',
    'font' => 2,
    'align' => 1
]);

// Play buzzer
$device->playBuzzer(200, 100, 600);
```

## Examples

### System Settings

```php
// Get all settings
$settings = $device->getSettings();
print_r($settings);

// Set device time to current time
$device->setDeviceTime();

// Set timezone
$device->setTimezone('GMT-5');

// Set temperature mode (0=Celsius, 1=Fahrenheit)
$device->setTemperatureMode(0);

// Set time format (0=12-hour, 1=24-hour)
$device->setTimeFormat(1);

// Turn screen on/off
$device->setScreenPower(true);  // On
$device->setScreenPower(false); // Off

// Set weather location (New York)
$device->setWeatherLocation(40.7128, -74.0060);
```

### Display Control

```php
// Get channel information
$channelInfo = $device->getChannelInfo();

// Set clock face for all displays
$device->setWholeDial(61);

// Set individual LCD panel clock
$device->setIndividualDial(1, 61); // Panel 1, Clock ID 61
```

### Text and Animation

```php
// Display scrolling text
$device->sendText('Welcome!', [
    'color' => '#00FF00',
    'speed' => 50,
    'font' => 3,
    'x' => 0,
    'y' => 0
]);

// Clear text
$device->clearText(1); // Clear text ID 1
$device->clearText(-1); // Clear all text

// Play GIF from URL
$device->playGif('http://example.com/animation.gif');
```

### Tools

```php
// Countdown timer (5 minutes 30 seconds)
$device->setCountdown(5, 30, true);

// Stopwatch
$device->setStopwatch(true);  // Start
$device->setStopwatch(false); // Stop

// Scoreboard
$device->setScoreboard(12, 8); // Red: 12, Blue: 8

// Noise meter
$device->setNoiseMeter(true);  // Enable
$device->setNoiseMeter(false); // Disable
```

### Raw Commands

```php
// Send any command directly
$response = $device->sendRawCommand([
    'Command' => 'Device/PlayBuzzer',
    'ActiveTimeInCycle' => 100,
    'OffTimeInCycle' => 100,
    'PlayTotalTime' => 500
]);
```

## Error Handling

```php
use Divoom\TimesGate\TimesGateException;

try {
    $device->setBrightness(75);
} catch (TimesGateException $e) {
    echo "Error: " . $e->getMessage();
}
```

## API Reference

See the [complete API documentation](../docs/API_REFERENCE.md) for all available commands.

## License

MIT License 