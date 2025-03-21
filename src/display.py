import argparse
from divoom_times_gate import DivoomTimesGate

def create_display_list(
    text="hello, divoom", 
    text_color="#FFFFFF", 
    text_x=16,
    text_y=16,
    text_width=48,
    text_height=16,
    text_font=2,
    text_speed=100,
    text_align=1,
    date_color="#FFF000",
    date_url="http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0",
    date_x=0,
    date_y=48,
    date_width=64,
    date_height=16,
    date_font=4,
    date_speed=100,
    date_align=1,
    date_update_time=60,
    center_color="#FF0000",
    center_x=32,
    center_y=32,
    topleft_color="#FF0000",
    topleft_x=0,
    topleft_y=0
):
    """Create a display list with customizable parameters."""
    return [
        # Center item (type 6)
        {
            "TextId": 5,
            "type": 6,
            "x": center_x,
            "y": center_y,
            "dir": 0,
            "font": 18,
            "TextWidth": 32,
            "Textheight": 16,
            "speed": 100,
            "align": 1,
            "color": center_color
        },
        # Top-left item (type 14)
        {
            "TextId": 1,
            "type": 14,
            "x": topleft_x,
            "y": topleft_y,
            "dir": 0,
            "font": 18,
            "TextWidth": 32,
            "Textheight": 16,
            "speed": 100,
            "align": 1,
            "color": topleft_color
        },
        # Custom text message
        {
            "TextId": 2,
            "type": 22,
            "x": text_x,
            "y": text_y,
            "dir": 0,
            "font": text_font,
            "TextWidth": text_width,
            "Textheight": text_height,
            "speed": text_speed,
            "align": text_align,
            "TextString": text,
            "color": text_color
        },
        # Date display
        {
            "TextId": 20,
            "type": 23,
            "x": date_x,
            "y": date_y,
            "dir": 0,
            "font": date_font,
            "TextWidth": date_width,
            "Textheight": date_height,
            "speed": date_speed,
            "update_time": date_update_time,
            "align": date_align,
            "TextString": date_url,
            "color": date_color
        }
    ]

def main():
    parser = argparse.ArgumentParser(description='Control Divoom Times Gate display')
    
    # Basic parameters
    parser.add_argument('--lcd-index', type=int, default=1,
                      help='LCD panel index (default: 1)')
    parser.add_argument('--new-flag', type=int, default=1,
                      help='New flag (default: 1)')
    parser.add_argument('--background', 
                      default='http://f.divoom-gz.com/64_64.gif',
                      help='Background GIF URL')
    
    # Text parameters
    parser.add_argument('--text', default='hello, divoom',
                      help='Text to display (default: hello, divoom)')
    parser.add_argument('--text-color', default='#FFFFFF',
                      help='Color for main text (default: #FFFFFF)')
    parser.add_argument('--text-x', type=int, default=16,
                      help='X position for text (default: 16)')
    parser.add_argument('--text-y', type=int, default=16,
                      help='Y position for text (default: 16)')
    parser.add_argument('--text-width', type=int, default=48,
                      help='Width for text (default: 48)')
    parser.add_argument('--text-height', type=int, default=16,
                      help='Height for text (default: 16)')
    parser.add_argument('--text-font', type=int, default=2,
                      help='Font for text (default: 2)')
    parser.add_argument('--text-speed', type=int, default=100,
                      help='Speed for text (default: 100)')
    parser.add_argument('--text-align', type=int, default=1,
                      help='Alignment for text (default: 1)')
    
    # Date parameters
    parser.add_argument('--date-color', default='#FFF000',
                      help='Color for date display (default: #FFF000)')
    parser.add_argument('--date-url', 
                      default='http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0',
                      help='URL for date/time data (default: Divoom API)')
    parser.add_argument('--date-x', type=int, default=0,
                      help='X position for date (default: 0)')
    parser.add_argument('--date-y', type=int, default=48,
                      help='Y position for date (default: 48)')
    parser.add_argument('--date-width', type=int, default=64,
                      help='Width for date (default: 64)')
    parser.add_argument('--date-height', type=int, default=16,
                      help='Height for date (default: 16)')
    parser.add_argument('--date-font', type=int, default=4,
                      help='Font for date (default: 4)')
    parser.add_argument('--date-speed', type=int, default=100,
                      help='Speed for date (default: 100)')
    parser.add_argument('--date-align', type=int, default=1,
                      help='Alignment for date (default: 1)')
    parser.add_argument('--date-update-time', type=int, default=60,
                      help='Update time for date in seconds (default: 60)')
    
    # Center item parameters
    parser.add_argument('--center-color', default='#FF0000',
                      help='Color for center item (default: #FF0000)')
    parser.add_argument('--center-x', type=int, default=32,
                      help='X position for center item (default: 32)')
    parser.add_argument('--center-y', type=int, default=32,
                      help='Y position for center item (default: 32)')
    
    # Top-left item parameters
    parser.add_argument('--topleft-color', default='#FF0000',
                      help='Color for top-left item (default: #FF0000)')
    parser.add_argument('--topleft-x', type=int, default=0,
                      help='X position for top-left item (default: 0)')
    parser.add_argument('--topleft-y', type=int, default=0,
                      help='Y position for top-left item (default: 0)')

    args = parser.parse_args()

    # Create an instance of the DivoomTimesGate class
    divoom = DivoomTimesGate()

    # Create the item list with all customizable parameters
    item_list = create_display_list(
        # Text parameters
        text=args.text,
        text_color=args.text_color,
        text_x=args.text_x,
        text_y=args.text_y,
        text_width=args.text_width,
        text_height=args.text_height,
        text_font=args.text_font,
        text_speed=args.text_speed,
        text_align=args.text_align,
        
        # Date parameters
        date_color=args.date_color,
        date_url=args.date_url,
        date_x=args.date_x,
        date_y=args.date_y,
        date_width=args.date_width,
        date_height=args.date_height,
        date_font=args.date_font,
        date_speed=args.date_speed,
        date_align=args.date_align,
        date_update_time=args.date_update_time,
        
        # Center item parameters
        center_color=args.center_color,
        center_x=args.center_x,
        center_y=args.center_y,
        
        # Top-left item parameters
        topleft_color=args.topleft_color,
        topleft_x=args.topleft_x,
        topleft_y=args.topleft_y
    )

    # Send the display configuration
    response = divoom.send_display_list(
        lcd_index=args.lcd_index,
        new_flag=args.new_flag,
        background_gif=args.background,
        item_list=item_list
    )
    
    if response:
        print(f"Display updated successfully: {response}")
    else:
        print("Failed to update display")

if __name__ == "__main__":
    main() 