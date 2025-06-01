#!/usr/bin/env python3
"""
Simple synchronous brightness test for Times Gate.
"""

import requests
import time
import json


def test_brightness():
    """Test brightness control with simple requests."""
    device_ip = "192.168.68.50"
    url = f"http://{device_ip}:80/post"
    
    print(f"Testing Times Gate at {device_ip}...")
    
    # Get current settings
    print("\nGetting current settings...")
    response = requests.post(url, json={"Command": "Channel/GetAllConf"})
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    current_brightness = data.get("Brightness", "Unknown")
    print(f"Current brightness: {current_brightness}")
    
    # Test brightness levels
    test_levels = [25, 50, 75, 100, 50]
    
    for level in test_levels:
        print(f"\nSetting brightness to {level}%...")
        response = requests.post(url, json={
            "Command": "Channel/SetBrightness",
            "Brightness": level
        })
        print(f"Response: {response.json()}")
        
        if response.json().get("error_code") == 0:
            print(f"✓ Brightness set to {level}%")
        else:
            print(f"✗ Failed to set brightness")
        
        time.sleep(2)  # Wait 2 seconds between changes
    
    print("\nBrightness test complete!")
    
    # Beep to indicate completion
    print("Playing completion buzzer...")
    response = requests.post(url, json={
        "Command": "Device/PlayBuzzer",
        "ActiveTimeInCycle": 200,
        "OffTimeInCycle": 100,
        "PlayTotalTime": 600
    })
    print(f"Buzzer response: {response.json()}")


if __name__ == "__main__":
    test_brightness() 