#!/usr/bin/env python3
"""
Identify which LCD panel is which by displaying different content.
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divoom_timesgate import TimesGateDevice


async def test_panel_identification():
    """Display different content on each panel to identify them."""
    device_ip = os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')
    
    print("🔢 Panel Identification Test")
    print(f"📍 Device: {device_ip}")
    print("\nDisplaying different content on each panel...\n")
    
    async with TimesGateDevice(device_ip) as device:
        # First, clear everything
        print("1. Clearing all displays...")
        await device.set_noise_meter(False)
        await device.set_countdown(0, 0, start=False)
        await asyncio.sleep(1)
        
        # Get current channel config
        result = await device.send_raw_command({"Command": "Channel/GetIndex"})
        channels = result.get('SelectIndex', [])
        print(f"   Current channels: {channels}")
        print("   (VU meter is on channel 2, clocks on channel 0)")
        
        # Now set different scores on each panel
        print("\n2. Setting different scoreboards on each panel...")
        print("   This will help identify which panel is which number\n")
        
        panels = [
            {"id": 1, "red": 11, "blue": 11},
            {"id": 2, "red": 22, "blue": 22},
            {"id": 3, "red": 33, "blue": 33},
            {"id": 4, "red": 44, "blue": 44},
            {"id": 5, "red": 55, "blue": 55},
        ]
        
        for panel in panels:
            try:
                result = await device.send_raw_command({
                    "Command": "Tools/SetScoreBoard",
                    "RedScore": panel["red"],
                    "BlueScore": panel["blue"],
                    "LcdId": panel["id"]
                })
                print(f"   Panel {panel['id']}: Scoreboard {panel['red']}-{panel['blue']} ✓")
            except Exception as e:
                print(f"   Panel {panel['id']}: Failed - {e}")
        
        print("\n   Waiting 10 seconds to observe...")
        await asyncio.sleep(10)
        
        # Now try timers
        print("\n3. Setting different timers on each panel...")
        
        timer_configs = [
            {"id": 1, "min": 0, "sec": 10},
            {"id": 2, "min": 0, "sec": 20},
            {"id": 3, "min": 0, "sec": 30},
            {"id": 4, "min": 0, "sec": 40},
            {"id": 5, "min": 0, "sec": 50},
        ]
        
        for config in timer_configs:
            try:
                result = await device.send_raw_command({
                    "Command": "Tools/SetTimer",
                    "Minute": config["min"],
                    "Second": config["sec"],
                    "Status": 1,
                    "LcdId": config["id"]
                })
                print(f"   Panel {config['id']}: Timer 0:{config['sec']:02d} ✓")
            except Exception as e:
                print(f"   Panel {config['id']}: Failed - {e}")
        
        print("\n   Waiting 10 seconds to observe...")
        await asyncio.sleep(10)
        
        # Clear everything
        print("\n4. Clearing all timers...")
        await device.set_countdown(0, 0, start=False)
        
        print("\n✅ Test complete!")
        print("\n📊 RESULTS:")
        print("If your panels are arranged horizontally [1][2][3][4][5], you should have seen:")
        print("- First: Scoreboards showing 11-11, 22-22, 33-33, 44-44, 55-55")
        print("- Then: Timers showing 0:10, 0:20, 0:30, 0:40, 0:50")
        print("\nBased on what you saw, which panel showed which number?")
        print("This will help us understand the actual panel numbering.")


if __name__ == "__main__":
    asyncio.run(test_panel_identification()) 