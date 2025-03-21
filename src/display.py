import argparse
from divoom_times_gate import DivoomTimesGate

def create_display_list(text="hello, divoom", text_color="#FFFFFF", date_color="#FFF000"):
    """Create a display list with default settings and some customizable parameters."""
    return [
        # Center item (type 6)
        {
            "TextId": 5,
            "type": 6,
            "x": 32,
            "y": 32,
            "dir": 0,
            "font": 18,
            "TextWidth": 32,
            "Textheight": 16,
            "speed": 100,
            "align": 1,
            "color": "#FF0000"
        },
        # Top-left item (type 14)
        {
            "TextId": 1,
            "type": 14,
            "x": 0,
            "y": 0,
            "dir": 0,
            "font": 18,
            "TextWidth": 32,
            "Textheight": 16,
            "speed": 100,
            "align": 1,
            "color": "#FF0000"
        },
        # Custom text message
        {
            "TextId": 2,
            "type": 22,
            "x": 16,
            "y": 16,
            "dir": 0,
            "font": 2,
            "TextWidth": 48,
            "Textheight": 16,
            "speed": 100,
            "align": 1,
            "TextString": text,
            "color": text_color
        },
        # Date display
        {
            "TextId": 20,
            "type": 23,
            "x": 0,
            "y": 48,
            "dir": 0,
            "font": 4,
            "TextWidth": 64,
            "Textheight": 16,
            "speed": 100,
            "update_time": 60,
            "align": 1,
            "TextString": "http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0",
            "color": date_color
        }
    ]

def main():
    parser = argparse.ArgumentParser(description='Control Divoom Times Gate display')
    parser.add_argument('--text', default='hello, divoom',
                      help='Text to display (default: hello, divoom)')
    parser.add_argument('--text-color', default='#FFFFFF',
                      help='Color for main text (default: #FFFFFF)')
    parser.add_argument('--date-color', default='#FFF000',
                      help='Color for date display (default: #FFF000)')
    parser.add_argument('--lcd-index', type=int, default=1,
                      help='LCD panel index (default: 1)')
    parser.add_argument('--background', 
                      default='http://f.divoom-gz.com/64_64.gif',
                      help='Background GIF URL')

    args = parser.parse_args()

    # Create an instance of the DivoomTimesGate class
    divoom = DivoomTimesGate()

    # Create the display configuration
    display_data = {
        "LcdIndex": args.lcd_index,
        "NewFlag": 1,
        "BackgroudGif": args.background,
        "ItemList": create_display_list(
            text=args.text,
            text_color=args.text_color,
            date_color=args.date_color
        )
    }

    # Send the display configuration
    response = divoom.send_display_list(**display_data)
    if response:
        print(f"Display updated successfully: {response}")
    else:
        print("Failed to update display")

if __name__ == "__main__":
    main() 