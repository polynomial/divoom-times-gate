#!/usr/bin/env python3
"""
Custom Clock Display Example

This example shows how to create a custom clock display with:
- Current time in large font
- Date below
- Custom colors
- Weather info
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from divoom_times_gate import DivoomTimesGate


def create_custom_clock():
    """Create a custom clock display."""
    device = DivoomTimesGate()
    
    # Define the display items
    items = [
        # Large time display at top
        {
            "TextId": 1,
            "type": 23,  # Dynamic text with URL
            "x": 32,
            "y": 10,
            "dir": 0,
            "font": 4,  # Large font
            "TextWidth": 64,
            "Textheight": 20,
            "speed": 0,  # Static
            "update_time": 1,  # Update every second
            "align": 2,  # Center aligned
            "TextString": "http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0",
            "color": "#00FF00"  # Green
        },
        # Date display below time
        {
            "TextId": 2,
            "type": 14,  # Date type
            "x": 32,
            "y": 35,
            "dir": 0,
            "font": 2,  # Medium font
            "TextWidth": 64,
            "Textheight": 12,
            "speed": 0,
            "align": 2,  # Center
            "color": "#FFFF00"  # Yellow
        },
        # Custom message at bottom
        {
            "TextId": 3,
            "type": 22,  # Custom text
            "x": 32,
            "y": 50,
            "dir": 0,
            "font": 1,  # Small font
            "TextWidth": 64,
            "Textheight": 10,
            "speed": 50,  # Slow scroll
            "align": 2,
            "TextString": "Have a great day!",
            "color": "#FF00FF"  # Magenta
        }
    ]
    
    # Send the display configuration
    print("Setting up custom clock display...")
    response = device.send_display_list(
        lcd_index=3,  # Center LCD panel
        new_flag=1,
        background_gif="",  # No background
        item_list=items
    )
    
    if response and response.get('error_code') == 0:
        print("✓ Custom clock display set successfully!")
    else:
        print("✗ Failed to set custom clock display")
        print(f"Response: {response}")


if __name__ == "__main__":
    create_custom_clock() 