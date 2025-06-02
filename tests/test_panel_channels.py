#!/usr/bin/env python3
"""
Test panel channel configuration for Times Gate.
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divoom_timesgate import TimesGateDevice


async def test_panel_channels():
    """Test and modify panel channel configuration."""
    device_ip = os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')
    
    print("📺 Times Gate Panel Channel Test")
    print(f"📍 Device: {device_ip}")
    print("\nExploring panel channels...\n")
    
    async with TimesGateDevice(device_ip) as device:
        # 1. Get current channel configuration
        print("1. Current channel configuration:")
        result = await device.send_raw_command({"Command": "Channel/GetIndex"})
        channels = result.get('SelectIndex', [])
        print(f"   Channel indices: {channels}")
        print("\n   Panel layout:")
        print("        [2]")
        print("     [1][5][3]")
        print("        [4]")
        print(f"\n   Current mapping:")
        if len(channels) >= 5:
            print(f"   Panel 1 (left):   Channel {channels[0]}")
            print(f"   Panel 2 (top):    Channel {channels[1]}")
            print(f"   Panel 3 (right):  Channel {channels[2]}")
            print(f"   Panel 4 (bottom): Channel {channels[3]}")
            print(f"   Panel 5 (center): Channel {channels[4]}")
            
            # Identify which panels have channel 2 (possibly VU meter)
            vu_panels = [i+1 for i, ch in enumerate(channels) if ch == 2]
            if vu_panels:
                print(f"\n   ⚠️  Panels {vu_panels} are on channel 2 (possibly VU meter)")
        
        # 2. Try to set all panels to channel 0
        print("\n2. Setting all panels to channel 0...")
        for i in range(5):
            try:
                # Try SetLcdIndex command
                result = await device.send_raw_command({
                    "Command": "Channel/SetLcdIndex",
                    "LcdIndex": i,
                    "SelectIndex": 0
                })
                print(f"   Panel {i}: {result}")
            except Exception as e:
                # Try alternative command format
                try:
                    result = await device.send_raw_command({
                        "Command": "Channel/SetPanelIndex",
                        "PanelId": i,
                        "ChannelId": 0
                    })
                    print(f"   Panel {i}: {result}")
                except:
                    print(f"   Panel {i}: Failed - {str(e)[:40]}")
        
        # 3. Check if configuration changed
        print("\n3. Checking new configuration...")
        result = await device.send_raw_command({"Command": "Channel/GetIndex"})
        new_channels = result.get('SelectIndex', [])
        print(f"   New channel indices: {new_channels}")
        
        if channels != new_channels:
            print("   ✓ Configuration changed!")
        else:
            print("   ✗ Configuration unchanged")
        
        # 4. Try text display now
        print("\n4. Testing text display after channel change...")
        await device.set_noise_meter(False)  # Make sure noise meter is off
        await device.clear_text(-1)
        
        # Send text to different positions
        text_tests = [
            {"text": "LEFT", "x": 0, "y": 8, "text_id": 1},
            {"text": "TOP", "x": 20, "y": 0, "text_id": 2},
            {"text": "RIGHT", "x": 40, "y": 8, "text_id": 3},
            {"text": "BOTTOM", "x": 20, "y": 16, "text_id": 4},
            {"text": "CENTER", "x": 20, "y": 8, "text_id": 5},
        ]
        
        for test in text_tests:
            try:
                await device.send_text(**test, color="#FFFFFF")
                print(f"   ✓ Sent '{test['text']}' to position ({test['x']}, {test['y']})")
            except Exception as e:
                print(f"   ✗ Failed to send '{test['text']}': {str(e)[:30]}")
        
        # 5. Try setting individual panels to different modes
        print("\n5. Testing individual panel control...")
        
        # Try to find a command that works for individual panel control
        test_commands = [
            {"desc": "SetIndividualChannel", "cmd": lambda i: {
                "Command": "Channel/SetIndividualChannel",
                "PanelIndex": i,
                "ChannelIndex": 0
            }},
            {"desc": "SetLcdChannel", "cmd": lambda i: {
                "Command": "Channel/SetLcdChannel", 
                "LcdId": i,
                "ChannelId": 0
            }},
            {"desc": "Draw/SetLcdIndex", "cmd": lambda i: {
                "Command": "Draw/SetLcdIndex",
                "Index": i,
                "Channel": 0
            }}
        ]
        
        for test in test_commands:
            print(f"\n   Trying {test['desc']}...")
            success = False
            for i in range(5):
                try:
                    result = await device.send_raw_command(test['cmd'](i))
                    if result.get('error_code', -1) == 0:
                        success = True
                        print(f"     Panel {i}: ✓")
                except:
                    print(f"     Panel {i}: ✗")
            if success:
                print(f"   {test['desc']} might work!")
                break
        
        # Final channel check
        print("\n6. Final channel configuration:")
        result = await device.send_raw_command({"Command": "Channel/GetIndex"})
        final_channels = result.get('SelectIndex', [])
        print(f"   Final channel indices: {final_channels}")
        
        print("\n" + "="*50)
        print("ANALYSIS:")
        print(f"Original channels: {channels}")
        print(f"Final channels:    {final_channels}")
        print("\nIf panels switched from channel 2 to 0, text might now be visible!")
        print("Check your device to see if any text is displayed.")


if __name__ == "__main__":
    asyncio.run(test_panel_channels()) 