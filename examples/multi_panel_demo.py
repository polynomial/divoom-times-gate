#!/usr/bin/env python3
"""
Multi-panel demo for Divoom Times Gate.
Shows different content on each of the 5 LCD panels.
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divoom_timesgate import TimesGateDevice


async def countdown_race():
    """Show a countdown race across all panels."""
    async with TimesGateDevice(os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')) as device:
        print("🏁 Countdown Race Demo")
        print("Watch all 5 panels count down at different speeds!\n")
        
        # Turn off noise meters
        await device.set_noise_meter(False)
        
        # Set different countdown times
        timers = [
            {"panel": 1, "seconds": 10, "name": "Panel 1 (10s)"},
            {"panel": 2, "seconds": 20, "name": "Panel 2 (20s)"},
            {"panel": 3, "seconds": 30, "name": "Panel 3 (30s)"},
            {"panel": 4, "seconds": 40, "name": "Panel 4 (40s)"},
            {"panel": 5, "seconds": 50, "name": "Panel 5 (50s)"},
        ]
        
        print("Starting timers:")
        for timer in timers:
            await device.set_panel_timer(
                panel=timer["panel"],
                minutes=0,
                seconds=timer["seconds"],
                start=True
            )
            print(f"  ✓ {timer['name']}")
        
        print("\nTimers are running! Watch them count down...")
        print("Press Ctrl+C to stop\n")
        
        try:
            await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("\nStopping timers...")
            for i in range(1, 6):
                await device.set_panel_timer(i, 0, 0, start=False)


async def sports_scores():
    """Display different game scores on each panel."""
    async with TimesGateDevice(os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')) as device:
        print("🏀 Sports Scores Demo")
        print("Showing different game scores on each panel\n")
        
        # Turn off noise meters
        await device.set_noise_meter(False)
        
        games = [
            {"panel": 1, "red": 98, "blue": 95, "sport": "Basketball"},
            {"panel": 2, "red": 3, "blue": 2, "sport": "Soccer"},
            {"panel": 3, "red": 21, "blue": 17, "sport": "Football"},
            {"panel": 4, "red": 6, "blue": 4, "sport": "Hockey"},
            {"panel": 5, "red": 15, "blue": 12, "sport": "Tennis"},
        ]
        
        print("Game scores:")
        for game in games:
            await device.set_panel_scoreboard(
                panel=game["panel"],
                red_score=game["red"],
                blue_score=game["blue"]
            )
            print(f"  Panel {game['panel']}: {game['sport']} - Red {game['red']} vs Blue {game['blue']}")
        
        print("\nScores displayed! Press Enter to clear...")
        input()
        
        # Clear by setting all to 0-0
        for i in range(1, 6):
            await device.set_panel_scoreboard(i, 0, 0)


async def panel_wave():
    """Create a wave effect across panels using timers."""
    async with TimesGateDevice(os.environ.get('DIVOOM_TIMES_GATE_IP', '192.168.68.50')) as device:
        print("🌊 Panel Wave Demo")
        print("Creating a wave effect across all panels\n")
        
        # Turn off noise meters
        await device.set_noise_meter(False)
        
        print("Watch the wave move across the panels...")
        
        for wave in range(3):  # 3 waves
            print(f"\nWave {wave + 1}:")
            
            # Start timers in sequence
            for panel in range(1, 6):
                await device.set_panel_timer(panel, 0, 5, start=True)
                print(f"  Panel {panel} ▶", end="", flush=True)
                await asyncio.sleep(0.5)
            
            # Wait for timers to finish
            await asyncio.sleep(6)
            
            # Clear all
            for panel in range(1, 6):
                await device.set_panel_timer(panel, 0, 0, start=False)
        
        print("\n\n✨ Wave complete!")


async def main():
    """Run all demos."""
    demos = [
        ("Countdown Race", countdown_race),
        ("Sports Scores", sports_scores),
        ("Panel Wave", panel_wave),
    ]
    
    print("🎮 Divoom Times Gate Multi-Panel Demo")
    print("=====================================\n")
    print("Available demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"{i}. {name}")
    print("0. Exit\n")
    
    while True:
        try:
            choice = input("Select demo (0-3): ")
            choice = int(choice)
            
            if choice == 0:
                print("Goodbye!")
                break
            elif 1 <= choice <= len(demos):
                print(f"\n{'='*50}\n")
                await demos[choice-1][1]()
                print(f"\n{'='*50}\n")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a number!")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 