#!/usr/bin/env python3
"""
Test script for Times Gate brightness control.
"""

import asyncio
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divoom_timesgate import TimesGateDevice

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)


async def test_brightness():
    """Test brightness control."""
    device_ip = "192.168.68.50"
    
    print(f"Connecting to Times Gate at {device_ip}...")
    
    async with TimesGateDevice(device_ip) as device:
        # Get current settings
        print("\nGetting current settings...")
        settings = await device.get_settings()
        current_brightness = settings.get("Brightness", "Unknown")
        print(f"Current brightness: {current_brightness}")
        
        # Test brightness levels
        test_levels = [25, 50, 75, 100, 50]
        
        for level in test_levels:
            print(f"\nSetting brightness to {level}%...")
            await device.set_brightness(level)
            print(f"✓ Brightness set to {level}%")
            await asyncio.sleep(2)  # Wait 2 seconds between changes
        
        print("\nBrightness test complete!")
        
        # Beep to indicate completion
        print("Playing completion buzzer...")
        await device.play_buzzer(on_time=200, off_time=100, total_time=600)


if __name__ == "__main__":
    asyncio.run(test_brightness()) 