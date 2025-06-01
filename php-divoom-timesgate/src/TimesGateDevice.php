<?php

namespace Divoom\TimesGate;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;

/**
 * Main class for controlling a Divoom Times Gate device.
 */
class TimesGateDevice
{
    /** @var string */
    private $ipAddress;
    
    /** @var int */
    private $port;
    
    /** @var string */
    private $baseUrl;
    
    /** @var Client */
    private $httpClient;
    
    /**
     * Initialize a Times Gate device connection.
     *
     * @param string $ipAddress IP address of the device
     * @param int $port HTTP port (default: 80)
     */
    public function __construct(string $ipAddress, int $port = 80)
    {
        $this->ipAddress = $ipAddress;
        $this->port = $port;
        $this->baseUrl = "http://{$ipAddress}:{$port}/post";
        
        $this->httpClient = new Client([
            'timeout' => 10,
            'headers' => [
                'Content-Type' => 'application/json',
            ],
        ]);
    }
    
    /**
     * Send a command to the device.
     *
     * @param array $command Command array to send
     * @return array Response from the device
     * @throws TimesGateException
     */
    private function sendCommand(array $command): array
    {
        try {
            $response = $this->httpClient->post($this->baseUrl, [
                'json' => $command,
            ]);
            
            $data = json_decode($response->getBody()->getContents(), true);
            
            if (($data['error_code'] ?? -1) !== 0) {
                throw new TimesGateException(
                    "Command failed with error code: " . ($data['error_code'] ?? 'unknown')
                );
            }
            
            return $data;
            
        } catch (GuzzleException $e) {
            throw new TimesGateException("Failed to connect to device: " . $e->getMessage(), 0, $e);
        }
    }
    
    // System Settings
    
    /**
     * Set the display brightness.
     *
     * @param int $brightness Brightness level (0-100)
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setBrightness(int $brightness): bool
    {
        if ($brightness < 0 || $brightness > 100) {
            throw new \InvalidArgumentException("Brightness must be between 0 and 100");
        }
        
        $this->sendCommand([
            'Command' => 'Channel/SetBrightness',
            'Brightness' => $brightness,
        ]);
        
        return true;
    }
    
    /**
     * Get all device settings.
     *
     * @return array Device settings
     * @throws TimesGateException
     */
    public function getSettings(): array
    {
        return $this->sendCommand([
            'Command' => 'Channel/GetAllConf',
        ]);
    }
    
    /**
     * Set the device time.
     *
     * @param int|null $timestamp Unix timestamp (default: current time)
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setDeviceTime(?int $timestamp = null): bool
    {
        if ($timestamp === null) {
            $timestamp = time();
        }
        
        $this->sendCommand([
            'Command' => 'Device/SetUTC',
            'Utc' => $timestamp,
        ]);
        
        return true;
    }
    
    /**
     * Get the device time.
     *
     * @return array Device time information
     * @throws TimesGateException
     */
    public function getDeviceTime(): array
    {
        return $this->sendCommand([
            'Command' => 'Device/GetDeviceTime',
        ]);
    }
    
    /**
     * Set the device timezone.
     *
     * @param string $timezone Timezone string (e.g., "GMT-5", "GMT+8")
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setTimezone(string $timezone): bool
    {
        $this->sendCommand([
            'Command' => 'Sys/TimeZone',
            'TimeZoneValue' => $timezone,
        ]);
        
        return true;
    }
    
    /**
     * Set temperature display mode.
     *
     * @param int $mode 0 = Celsius, 1 = Fahrenheit
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setTemperatureMode(int $mode): bool
    {
        $this->sendCommand([
            'Command' => 'Device/SetDisTempMode',
            'Mode' => $mode,
        ]);
        
        return true;
    }
    
    /**
     * Set display mirror mode.
     *
     * @param bool $enabled True to enable mirroring
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setMirrorMode(bool $enabled): bool
    {
        $this->sendCommand([
            'Command' => 'Device/SetMirrorMode',
            'Mode' => $enabled ? 1 : 0,
        ]);
        
        return true;
    }
    
    /**
     * Set time display format.
     *
     * @param int $format 0 = 12-hour, 1 = 24-hour
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setTimeFormat(int $format): bool
    {
        $this->sendCommand([
            'Command' => 'Device/SetTime24Flag',
            'Mode' => $format,
        ]);
        
        return true;
    }
    
    /**
     * Turn the display on or off.
     *
     * @param bool $on True to turn on, false to turn off
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setScreenPower(bool $on): bool
    {
        $this->sendCommand([
            'Command' => 'Channel/OnOffScreen',
            'OnOff' => $on ? 1 : 0,
        ]);
        
        return true;
    }
    
    /**
     * Set the weather location.
     *
     * @param float $latitude Latitude coordinate
     * @param float $longitude Longitude coordinate
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setWeatherLocation(float $latitude, float $longitude): bool
    {
        $this->sendCommand([
            'Command' => 'Sys/LogAndLat',
            'Latitude' => (string)$latitude,
            'Longitude' => (string)$longitude,
        ]);
        
        return true;
    }
    
    /**
     * Reboot the device.
     *
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function reboot(): bool
    {
        $this->sendCommand([
            'Command' => 'Device/Reboot',
        ]);
        
        return true;
    }
    
    // Display Control
    
    /**
     * Get current channel information.
     *
     * @return array Channel information
     * @throws TimesGateException
     */
    public function getChannelInfo(): array
    {
        return $this->sendCommand([
            'Command' => 'Channel/GetCurChannelInfo',
        ]);
    }
    
    /**
     * Set clock face for all displays.
     *
     * @param int $clockId ID of the clock face
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setWholeDial(int $clockId): bool
    {
        $this->sendCommand([
            'Command' => 'Channel/SetWholeDial',
            'ClockId' => $clockId,
        ]);
        
        return true;
    }
    
    /**
     * Set clock face for individual LCD panel.
     *
     * @param int $lcdId LCD panel index (1-5)
     * @param int $clockId Clock face ID
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setIndividualDial(int $lcdId, int $clockId): bool
    {
        $this->sendCommand([
            'Command' => 'Channel/SetIndividualDial',
            'LcdId' => $lcdId,
            'ClockId' => $clockId,
        ]);
        
        return true;
    }
    
    // Animation & Text
    
    /**
     * Display text on the device.
     *
     * @param string $text Text to display
     * @param array $options Optional parameters
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function sendText(string $text, array $options = []): bool
    {
        $command = array_merge([
            'Command' => 'Draw/SendHttpText',
            'TextString' => $text,
            'TextId' => $options['textId'] ?? 1,
            'x' => $options['x'] ?? 0,
            'y' => $options['y'] ?? 0,
            'dir' => $options['direction'] ?? 0,
            'font' => $options['font'] ?? 2,
            'TextWidth' => $options['width'] ?? 64,
            'speed' => $options['speed'] ?? 0,
            'color' => $options['color'] ?? '#FFFFFF',
            'align' => $options['align'] ?? 1,
        ], $options);
        
        $this->sendCommand($command);
        
        return true;
    }
    
    /**
     * Clear displayed text.
     *
     * @param int $textId Text ID to clear (-1 for all)
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function clearText(int $textId = -1): bool
    {
        $this->sendCommand([
            'Command' => 'Draw/ClearHttpText',
            'TextId' => $textId,
        ]);
        
        return true;
    }
    
    /**
     * Play a GIF animation from URL.
     *
     * @param string $url URL of the GIF file
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function playGif(string $url): bool
    {
        $this->sendCommand([
            'Command' => 'Device/PlayTFGif',
            'FileType' => 2,
            'FileName' => $url,
        ]);
        
        return true;
    }
    
    // Tools
    
    /**
     * Set countdown timer.
     *
     * @param int $minutes Minutes (0-99)
     * @param int $seconds Seconds (0-59)
     * @param bool $start True to start, false to stop
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setCountdown(int $minutes, int $seconds, bool $start = true): bool
    {
        $this->sendCommand([
            'Command' => 'Tools/SetTimer',
            'Minute' => $minutes,
            'Second' => $seconds,
            'Status' => $start ? 1 : 0,
        ]);
        
        return true;
    }
    
    /**
     * Control the stopwatch.
     *
     * @param bool $start True to start, false to stop/reset
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setStopwatch(bool $start): bool
    {
        $this->sendCommand([
            'Command' => 'Tools/SetStopWatch',
            'Status' => $start ? 1 : 0,
        ]);
        
        return true;
    }
    
    /**
     * Display a scoreboard.
     *
     * @param int $redScore Red team score (0-999)
     * @param int $blueScore Blue team score (0-999)
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setScoreboard(int $redScore, int $blueScore): bool
    {
        $this->sendCommand([
            'Command' => 'Tools/SetScoreBoard',
            'RedScore' => $redScore,
            'BlueScore' => $blueScore,
        ]);
        
        return true;
    }
    
    /**
     * Enable or disable noise meter.
     *
     * @param bool $enabled True to enable
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function setNoiseMeter(bool $enabled): bool
    {
        $this->sendCommand([
            'Command' => 'Tools/SetNoiseStatus',
            'Status' => $enabled ? 1 : 0,
        ]);
        
        return true;
    }
    
    /**
     * Sound the buzzer.
     *
     * @param int $onTime Buzzer on time in ms
     * @param int $offTime Buzzer off time in ms
     * @param int $totalTime Total duration in ms
     * @return bool True if successful
     * @throws TimesGateException
     */
    public function playBuzzer(int $onTime = 500, int $offTime = 500, int $totalTime = 2000): bool
    {
        $this->sendCommand([
            'Command' => 'Device/PlayBuzzer',
            'ActiveTimeInCycle' => $onTime,
            'OffTimeInCycle' => $offTime,
            'PlayTotalTime' => $totalTime,
        ]);
        
        return true;
    }
    
    /**
     * Send a raw command to the device.
     *
     * @param array $command Command array
     * @return array Response from the device
     * @throws TimesGateException
     */
    public function sendRawCommand(array $command): array
    {
        return $this->sendCommand($command);
    }
} 