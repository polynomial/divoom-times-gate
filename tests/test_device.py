#!/usr/bin/env python3
"""
Test suite for Divoom Times Gate device functionality.
"""

import pytest
import asyncio
import os
from divoom_timesgate import TimesGateDevice, TimesGateError


# Skip tests if no device IP is provided
DEVICE_IP = os.environ.get('DIVOOM_TIMES_GATE_IP')
pytestmark = pytest.mark.skipif(
    not DEVICE_IP, 
    reason="No DIVOOM_TIMES_GATE_IP environment variable set"
)


@pytest.fixture
async def device():
    """Create a device connection for testing."""
    async with TimesGateDevice(DEVICE_IP) as dev:
        yield dev


@pytest.mark.asyncio
async def test_connection(device):
    """Test basic device connection."""
    # If we get here without exception, connection works
    assert device.ip_address == DEVICE_IP
    assert device._session is not None


@pytest.mark.asyncio
async def test_brightness_control(device):
    """Test brightness adjustment."""
    # Set brightness to 50%
    result = await device.set_brightness(50)
    assert result is True
    
    # Get settings to verify
    settings = await device.get_settings()
    assert settings.get('Brightness') == 50
    
    # Test invalid brightness
    with pytest.raises(ValueError):
        await device.set_brightness(101)
    
    with pytest.raises(ValueError):
        await device.set_brightness(-1)


@pytest.mark.asyncio
async def test_screen_power(device):
    """Test screen power control."""
    # Turn off
    result = await device.set_screen_power(False)
    assert result is True
    
    await asyncio.sleep(1)
    
    # Turn on
    result = await device.set_screen_power(True) 
    assert result is True


@pytest.mark.asyncio
async def test_countdown_timer(device):
    """Test countdown timer functionality."""
    # Start 10 second timer
    result = await device.set_countdown(0, 10, start=True)
    assert result is True
    
    await asyncio.sleep(2)
    
    # Stop timer
    result = await device.set_countdown(0, 0, start=False)
    assert result is True


@pytest.mark.asyncio
async def test_scoreboard(device):
    """Test scoreboard display."""
    result = await device.set_scoreboard(10, 5)
    assert result is True
    
    await asyncio.sleep(2)
    
    # Clear by setting to 0
    result = await device.set_scoreboard(0, 0)
    assert result is True


@pytest.mark.asyncio  
async def test_panel_specific_timer(device):
    """Test panel-specific timer control."""
    # Set different timers on panels 1 and 3
    result = await device.set_panel_timer(panel=1, minutes=0, seconds=15)
    assert result is True
    
    result = await device.set_panel_timer(panel=3, minutes=0, seconds=30)
    assert result is True
    
    await asyncio.sleep(2)
    
    # Clear timers
    await device.set_countdown(0, 0, start=False)


@pytest.mark.asyncio
async def test_get_panel_channels(device):
    """Test getting panel channel information."""
    channels = await device.get_panel_channels()
    assert isinstance(channels, list)
    assert len(channels) == 5  # Should have 5 panels


@pytest.mark.asyncio
async def test_buzzer(device):
    """Test buzzer functionality."""
    # Short beep
    result = await device.play_buzzer(100, 100, 300)
    assert result is True


@pytest.mark.asyncio
async def test_raw_command(device):
    """Test sending raw commands."""
    # Get channel index - a safe read-only command
    result = await device.send_raw_command({
        "Command": "Channel/GetIndex"
    })
    assert result.get('error_code', -1) == 0
    assert 'SelectIndex' in result


if __name__ == "__main__":
    # Run with: python -m pytest tests/test_device.py -v
    pytest.main([__file__, "-v"]) 