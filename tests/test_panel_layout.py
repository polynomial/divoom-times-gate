#!/usr/bin/env python3
"""
Test script to identify the actual LCD panel layout of the Times Gate.
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divoom_timesgate import TimesGateDevice, DisplayPanel


async def test_panel_layout():
    """Test each LCD panel to identify the layout."""
    device_ip = os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')
    
    print("🔍 Times Gate LCD Panel Layout Test")
    print(f"📍 Device: {device_ip}")
    print("\nThis test will display a number on each LCD panel.")
    print("Please observe which panel shows which number.\n")
    
    async with TimesGateDevice(device_ip) as device:
        # First, get the current channel info
        channel_info = await device.get_channel_info()
        print(f"Channel Info: {channel_info}\n")
        
        # Test each panel if individual dial control is supported
        panels = [
            (DisplayPanel.LEFT, "1", "Panel 1 (LEFT)"),
            (DisplayPanel.TOP, "2", "Panel 2 (TOP)"),
            (DisplayPanel.RIGHT, "3", "Panel 3 (RIGHT)"),
            (DisplayPanel.BOTTOM, "4", "Panel 4 (BOTTOM)"),
            (DisplayPanel.CENTER, "5", "Panel 5 (CENTER)")
        ]
        
        print("Testing individual panels...")
        print("Each panel will show its number for 3 seconds.\n")
        
        for panel, number, description in panels:
            print(f"Testing {description}...")
            try:
                # Try to set individual dial with a specific clock ID
                # You might need to adjust the clock_id based on available clocks
                await device.set_individual_dial(panel, 61)  # 61 is often a digital clock
                
                # Display the panel number
                await device.send_text(
                    text=number,
                    text_id=panel.value,
                    color="#00FF00",
                    x=28,  # Center position for 64px display
                    y=24,
                    font=4  # Large font
                )
                
                await asyncio.sleep(3)
                
                # Clear the text
                await device.clear_text(panel.value)
                
                print(f"✓ {description} complete")
                
            except Exception as e:
                print(f"✗ {description} failed: {str(e)}")
            
            await asyncio.sleep(1)
        
        # Clear all text
        await device.clear_text(-1)
        
        print("\n📝 Test complete!")
        print("\nBased on what you observed:")
        print("- Which physical position showed '1'?")
        print("- Which physical position showed '2'?")
        print("- Which physical position showed '3'?")
        print("- Which physical position showed '4'?")
        print("- Which physical position showed '5'?")
        print("\nThis will help us map the correct layout!")


if __name__ == "__main__":
    asyncio.run(test_panel_layout()) 