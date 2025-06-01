#!/usr/bin/env python3
"""
Quick demo of Divoom Times Gate features.
"""

import asyncio
import sys
import os

# Add parent directory to path if running from examples/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divoom_timesgate import TimesGateDevice, TextAlignment, FontSize


async def main():
    """Run a quick demo of Times Gate features."""
    device_ip = os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')
    
    print(f"🎮 Divoom Times Gate Demo")
    print(f"📍 Connecting to device at {device_ip}...")
    
    async with TimesGateDevice(device_ip) as device:
        # 1. Show current settings
        print("\n📊 Current Settings:")
        settings = await device.get_settings()
        print(f"  • Brightness: {settings.get('Brightness')}%")
        print(f"  • Temperature: {'Celsius' if settings.get('TemperatureMode') == 0 else 'Fahrenheit'}")
        print(f"  • Time Format: {'24-hour' if settings.get('Time24Flag') == 1 else '12-hour'}")
        
        # 2. Brightness demo
        print("\n💡 Brightness Demo:")
        for level in [25, 75, 50]:
            print(f"  • Setting brightness to {level}%...")
            await device.set_brightness(level)
            await asyncio.sleep(1)
        
        # 3. Text display demo
        print("\n📝 Text Display Demo:")
        messages = [
            ("Hello!", "#FF0000", FontSize.LARGE),
            ("Times Gate", "#00FF00", FontSize.MEDIUM),
            ("Ready!", "#0000FF", FontSize.SMALL)
        ]
        
        for text, color, font in messages:
            print(f"  • Displaying: {text}")
            await device.send_text(text, color=color, font=font)
            await asyncio.sleep(2)
        
        # 4. Timer demo
        print("\n⏱️ Timer Demo:")
        print("  • Starting 10 second countdown...")
        await device.set_countdown(0, 10, True)
        await asyncio.sleep(5)
        print("  • Stopping timer")
        await device.set_countdown(0, 0, False)
        
        # 5. Buzzer finale
        print("\n🔔 Playing completion sound...")
        await device.play_buzzer(on_time=200, off_time=100, total_time=600)
        
        # Clear text
        await device.clear_text(-1)
        
        print("\n✅ Demo complete!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n�� Demo interrupted") 