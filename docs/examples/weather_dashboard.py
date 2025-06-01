#!/usr/bin/env python3
"""
Weather Dashboard Example

This example creates a comprehensive weather dashboard that displays:
- Current temperature
- Weather conditions
- Location
- Time and date
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from divoom_times_gate import DivoomTimesGate


def setup_weather_dashboard(latitude, longitude):
    """
    Set up a weather dashboard display.
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
    """
    device = DivoomTimesGate()
    
    # First, configure weather location
    print(f"Setting weather location to {latitude}°, {longitude}°...")
    response = device.set_weather_location(longitude, latitude)
    if response and response.get('error_code') == 0:
        print("✓ Weather location configured")
    else:
        print("✗ Failed to set weather location")
        return
    
    # Get current weather to display
    print("Fetching weather data...")
    weather_data = device.get_weather()
    if weather_data:
        print("✓ Weather data received:")
        print(json.dumps(weather_data, indent=2))
    
    # Create weather dashboard display
    # Note: This layout assumes a 64x64 pixel display for the center LCD
    items = [
        # Weather condition icon/text at top
        {
            "TextId": 1,
            "type": 6,  # Weather type display
            "x": 32,
            "y": 8,
            "dir": 0,
            "font": 2,
            "TextWidth": 64,
            "Textheight": 12,
            "speed": 0,
            "align": 2,
            "color": "#00FFFF"  # Cyan
        },
        # Temperature display (large)
        {
            "TextId": 2,
            "type": 14,  # Temperature display
            "x": 32,
            "y": 25,
            "dir": 0,
            "font": 4,  # Large font
            "TextWidth": 64,
            "Textheight": 20,
            "speed": 0,
            "align": 2,
            "color": "#FFFF00"  # Yellow
        },
        # Location name
        {
            "TextId": 3,
            "type": 22,
            "x": 32,
            "y": 45,
            "dir": 0,
            "font": 1,
            "TextWidth": 60,
            "Textheight": 10,
            "speed": 20,  # Scroll if long
            "align": 2,
            "TextString": "San Francisco",  # Replace with your city
            "color": "#FFFFFF"
        },
        # Current time at bottom
        {
            "TextId": 4,
            "type": 23,
            "x": 32,
            "y": 56,
            "dir": 0,
            "font": 1,
            "TextWidth": 64,
            "Textheight": 8,
            "speed": 0,
            "update_time": 60,
            "align": 2,
            "TextString": "http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0",
            "color": "#808080"  # Gray
        }
    ]
    
    # Send the weather dashboard configuration
    print("\nSetting up weather dashboard...")
    response = device.send_display_list(
        lcd_index=3,  # Center LCD panel
        new_flag=1,
        background_gif="",  # Could use a weather-themed background
        item_list=items
    )
    
    if response and response.get('error_code') == 0:
        print("✓ Weather dashboard configured successfully!")
        print("\nThe dashboard will automatically update with current weather data.")
    else:
        print("✗ Failed to configure weather dashboard")
        print(f"Response: {response}")


def create_multi_panel_weather():
    """Create a weather display across multiple LCD panels."""
    device = DivoomTimesGate()
    
    print("Creating multi-panel weather display...")
    
    # Panel 1 (Top-left): Current temperature
    panel1_items = [{
        "TextId": 1,
        "type": 14,  # Temperature
        "x": 32, "y": 32,
        "font": 4,
        "TextWidth": 64,
        "Textheight": 32,
        "align": 2,
        "color": "#FF6600"  # Orange
    }]
    
    # Panel 2 (Top-right): Weather condition
    panel2_items = [{
        "TextId": 1,
        "type": 6,  # Weather icon
        "x": 32, "y": 32,
        "font": 3,
        "TextWidth": 64,
        "Textheight": 32,
        "align": 2,
        "color": "#00CCFF"  # Sky blue
    }]
    
    # Panel 3 (Center): Time
    panel3_items = [{
        "TextId": 1,
        "type": 23,
        "x": 32, "y": 32,
        "font": 4,
        "TextWidth": 64,
        "Textheight": 32,
        "update_time": 1,
        "align": 2,
        "TextString": "http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0",
        "color": "#00FF00"  # Green
    }]
    
    # Panel 4 (Bottom-left): Min/Max temps
    panel4_items = [{
        "TextId": 1,
        "type": 22,
        "x": 32, "y": 32,
        "font": 2,
        "TextWidth": 64,
        "Textheight": 32,
        "align": 2,
        "TextString": "H:75° L:55°",
        "color": "#FFFFFF"
    }]
    
    # Panel 5 (Bottom-right): Location
    panel5_items = [{
        "TextId": 1,
        "type": 22,
        "x": 32, "y": 32,
        "font": 2,
        "TextWidth": 64,
        "Textheight": 32,
        "speed": 30,
        "align": 2,
        "TextString": "San Francisco, CA",
        "color": "#FFFF00"
    }]
    
    # Send configurations to all panels
    panels = [
        (1, panel1_items),
        (2, panel2_items),
        (3, panel3_items),
        (4, panel4_items),
        (5, panel5_items)
    ]
    
    for lcd_index, items in panels:
        response = device.send_display_list(
            lcd_index=lcd_index,
            new_flag=1,
            background_gif="",
            item_list=items
        )
        
        if response and response.get('error_code') == 0:
            print(f"✓ Panel {lcd_index} configured")
        else:
            print(f"✗ Failed to configure panel {lcd_index}")


if __name__ == "__main__":
    # Example: San Francisco coordinates
    # Replace with your location
    LATITUDE = 37.7749
    LONGITUDE = -122.4194
    
    print("Weather Dashboard Demo")
    print("=" * 50)
    
    # Set up single-panel weather dashboard
    setup_weather_dashboard(LATITUDE, LONGITUDE)
    
    # Uncomment to try multi-panel display
    # print("\n\nMulti-Panel Weather Display")
    # print("=" * 50)
    # create_multi_panel_weather() 