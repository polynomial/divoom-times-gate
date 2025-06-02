#!/usr/bin/env python3
"""
Automated discovery test for Times Gate text display.
"""

import asyncio
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divoom_timesgate import TimesGateDevice


async def test_auto_discovery():
    """Automatically test different approaches and verify results."""
    device_ip = os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')
    
    print("🤖 Times Gate Automated Discovery Test")
    print(f"📍 Device: {device_ip}")
    print("\nTrying different approaches automatically...\n")
    
    async with TimesGateDevice(device_ip) as device:
        results = {}
        
        # Test 1: Basic settings changes
        print("1. Testing basic settings...")
        try:
            # Change brightness
            await device.set_brightness(50)
            settings = await device.get_settings()
            brightness_works = settings.get('Brightness') == 50
            results['brightness_control'] = brightness_works
            print(f"   Brightness control: {'✓ WORKS' if brightness_works else '✗ FAILED'}")
            
            # Test screen power
            await device.set_screen_power(False)
            await asyncio.sleep(1)
            settings = await device.get_settings()
            screen_off = settings.get('LightSwitch') == 0
            
            await device.set_screen_power(True)
            await asyncio.sleep(1)
            settings = await device.get_settings()
            screen_on = settings.get('LightSwitch') == 1
            
            screen_control_works = screen_off and screen_on
            results['screen_control'] = screen_control_works
            print(f"   Screen power control: {'✓ WORKS' if screen_control_works else '✗ FAILED'}")
        except Exception as e:
            print(f"   Basic settings error: {e}")
        
        # Test 2: Try different raw commands to find valid ones
        print("\n2. Testing channel/mode commands...")
        working_commands = []
        
        test_commands = [
            {"name": "Channel/GetIndex", "cmd": {"Command": "Channel/GetIndex"}},
            {"name": "Channel/SetIndex 0", "cmd": {"Command": "Channel/SetIndex", "SelectIndex": 0}},
            {"name": "Channel/SetIndex 1", "cmd": {"Command": "Channel/SetIndex", "SelectIndex": 1}},
            {"name": "Channel/SetIndex 2", "cmd": {"Command": "Channel/SetIndex", "SelectIndex": 2}},
            {"name": "Device/GetAllChannel", "cmd": {"Command": "Device/GetAllChannel"}},
            {"name": "Channel/GetAllIndex", "cmd": {"Command": "Channel/GetAllIndex"}},
            {"name": "Draw/GetHttpTextList", "cmd": {"Command": "Draw/GetHttpTextList"}},
            {"name": "Device/GetDeviceChannelList", "cmd": {"Command": "Device/GetDeviceChannelList"}},
            {"name": "Channel/GetCustomPageIndex", "cmd": {"Command": "Channel/GetCustomPageIndex"}},
            {"name": "Tools/GetToolsStatus", "cmd": {"Command": "Tools/GetToolsStatus"}},
        ]
        
        for test in test_commands:
            try:
                result = await device.send_raw_command(test['cmd'])
                if result.get('error_code', -1) == 0:
                    working_commands.append(test['name'])
                    print(f"   ✓ {test['name']}: {json.dumps(result, separators=(',', ':'))[:60]}...")
                else:
                    print(f"   ✗ {test['name']}: Error {result.get('error_code')}")
            except Exception as e:
                print(f"   ✗ {test['name']}: {str(e)[:40]}")
        
        results['working_commands'] = working_commands
        
        # Test 3: Try text with different parameters
        print("\n3. Testing text display variations...")
        text_results = []
        
        text_tests = [
            {"desc": "Basic text", "params": {"text": "TEST", "text_id": 1}},
            {"desc": "Text ID 0", "params": {"text": "ID0", "text_id": 0}},
            {"desc": "Text with position", "params": {"text": "POS", "text_id": 1, "x": 0, "y": 0}},
            {"desc": "Scrolling text", "params": {"text": "SCROLL", "text_id": 1, "scroll_speed": 50}},
            {"desc": "Different colors", "params": {"text": "COLOR", "text_id": 1, "color": "#FF0000"}},
        ]
        
        for test in text_tests:
            try:
                await device.clear_text(-1)
                await device.send_text(**test['params'])
                
                # Try to verify if text was accepted
                # Some devices might have a command to list active texts
                try:
                    text_list = await device.send_raw_command({"Command": "Draw/GetHttpTextList"})
                    if text_list.get('error_code', -1) == 0:
                        text_results.append(f"{test['desc']}: Response={text_list}")
                except:
                    pass
                
                print(f"   ✓ {test['desc']}: Command accepted")
            except Exception as e:
                print(f"   ✗ {test['desc']}: {str(e)[:40]}")
        
        # Test 4: Find what tools/modes are available
        print("\n4. Testing available tools...")
        tools_working = []
        
        try:
            # Scoreboard
            await device.set_scoreboard(10, 5)
            tools_working.append("scoreboard")
            print("   ✓ Scoreboard works")
        except:
            print("   ✗ Scoreboard failed")
        
        try:
            # Timer
            await device.set_countdown(0, 10, start=True)
            await asyncio.sleep(1)
            await device.set_countdown(0, 0, start=False)
            tools_working.append("countdown")
            print("   ✓ Countdown timer works")
        except:
            print("   ✗ Countdown timer failed")
        
        try:
            # Stopwatch
            await device.set_stopwatch(True)
            await asyncio.sleep(1)
            await device.set_stopwatch(False)
            tools_working.append("stopwatch")
            print("   ✓ Stopwatch works")
        except:
            print("   ✗ Stopwatch failed")
        
        try:
            # Noise meter
            await device.set_noise_meter(True)
            await asyncio.sleep(1)
            await device.set_noise_meter(False)
            tools_working.append("noise_meter")
            print("   ✓ Noise meter control works")
        except:
            print("   ✗ Noise meter control failed")
        
        results['working_tools'] = tools_working
        
        # Test 5: Try to find the right sequence
        print("\n5. Testing command sequences...")
        sequences_tested = []
        
        # Sequence 1: Disable noise meter then text
        try:
            await device.set_noise_meter(False)
            await device.clear_text(-1)
            await device.send_text("AFTER NOISE OFF", text_id=1)
            sequences_tested.append("noise_off_then_text: ✓")
        except Exception as e:
            sequences_tested.append(f"noise_off_then_text: ✗ {str(e)[:30]}")
        
        # Sequence 2: Set channel 0 then text
        try:
            await device.send_raw_command({"Command": "Channel/SetIndex", "SelectIndex": 0})
            await device.clear_text(-1)
            await device.send_text("CHANNEL 0 TEXT", text_id=1)
            sequences_tested.append("channel_0_then_text: ✓")
        except Exception as e:
            sequences_tested.append(f"channel_0_then_text: ✗ {str(e)[:30]}")
        
        # Sequence 3: Command list with multiple operations
        try:
            commands = [
                {"Command": "Tools/SetNoiseStatus", "Status": 0},
                {"Command": "Draw/ClearHttpText", "TextId": -1},
                {"Command": "Draw/SendHttpText", "TextId": 1, "TextString": "CMDLIST", 
                 "x": 0, "y": 0, "color": "#FFFFFF", "font": 2, "align": 1, 
                 "speed": 0, "TextWidth": 64}
            ]
            await device.send_command_list(commands)
            sequences_tested.append("command_list: ✓")
        except Exception as e:
            sequences_tested.append(f"command_list: ✗ {str(e)[:30]}")
        
        for seq in sequences_tested:
            print(f"   {seq}")
        
        # Summary
        print("\n" + "="*50)
        print("SUMMARY:")
        print(f"Basic controls working: {results.get('brightness_control')} brightness, {results.get('screen_control')} screen")
        print(f"Working commands: {', '.join(results.get('working_commands', []))}")
        print(f"Working tools: {', '.join(results.get('working_tools', []))}")
        print("\nBased on results:")
        if 'scoreboard' in results.get('working_tools', []) or 'countdown' in results.get('working_tools', []):
            print("✓ Device can display custom content (tools work)")
        else:
            print("✗ Device might not support custom content")
        
        print("\nText display status: UNKNOWN - needs visual confirmation")
        print("The device accepts text commands but we can't verify display programmatically.")


if __name__ == "__main__":
    asyncio.run(test_auto_discovery()) 