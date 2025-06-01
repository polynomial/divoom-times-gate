#!/usr/bin/env python3
"""
Display List Demo

Demonstrates how to use display lists to create custom displays
with text and other elements on the Times Gate.
"""

import asyncio
from divoom_timesgate import (
    TimesGateDevice,
    TextDisplayItem,
    DateTimeDisplayItem
)


async def main():
    # Connect to your Times Gate device
    async with TimesGateDevice("192.168.68.50") as device:
        
        # Example 1: Simple text display
        print("Example 1: Simple text display")
        response = await device.create_text_display(
            text="Hello World!",
            panel=1,
            x=0,
            y=24,
            color="#00FF00",
            font=2
        )
        print(f"Response: {response}")
        
        await asyncio.sleep(3)
        
        # Example 2: Multiple items on one display
        print("\nExample 2: Multiple items display")
        
        # Create display items
        items = [
            # Main text message
            TextDisplayItem(
                text_id=1,
                text="Divoom Times Gate",
                x=0,
                y=10,
                color="#FF0000",
                font=2,
                width=64,
                height=16,
                speed=50,  # Scrolling text
                align=1
            ),
            
            # Secondary text
            TextDisplayItem(
                text_id=2,
                text="Python API",
                x=0,
                y=30,
                color="#0000FF",
                font=1,
                width=64,
                height=16,
                speed=0,  # Static text
                align=1
            ),
            
            # Date/time display at bottom
            DateTimeDisplayItem(
                text_id=3,
                x=0,
                y=48,
                color="#FFFF00",
                font=0,
                update_time=60
            )
        ]
        
        response = await device.create_multi_item_display(
            items=items,
            panel=1
        )
        print(f"Response: {response}")
        
        await asyncio.sleep(5)
        
        # Example 3: Using the low-level send_display_list directly
        print("\nExample 3: Low-level display list")
        
        # This is what was in the old display.py - custom item types
        custom_items = [
            {
                "TextId": 1,
                "type": 22,  # Custom text type
                "x": 0,
                "y": 20,
                "dir": 0,
                "font": 3,
                "TextWidth": 64,
                "Textheight": 24,
                "speed": 0,
                "align": 1,
                "TextString": "CUSTOM TEXT",
                "color": "#FFFFFF"
            }
        ]
        
        response = await device.send_display_list(
            lcd_index=1,
            new_flag=1,
            background_gif="",
            item_list=custom_items
        )
        print(f"Response: {response}")
        
        await asyncio.sleep(3)
        
        # Example 4: Different panels
        print("\nExample 4: Text on different panels")
        
        for panel in range(1, 6):
            await device.create_text_display(
                text=f"Panel {panel}",
                panel=panel,
                x=10,
                y=24,
                color="#FFFFFF",
                font=2
            )
            print(f"Set text on panel {panel}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main()) 