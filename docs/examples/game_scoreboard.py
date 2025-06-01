#!/usr/bin/env python3
"""
Game Scoreboard Example

This example shows how to create an interactive scoreboard for games with:
- Score tracking for two teams
- Timer functionality
- Victory celebrations
"""

import sys
import os
import time
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from divoom_times_gate import DivoomTimesGate


class GameScoreboard:
    """Interactive game scoreboard for Divoom Times Gate."""
    
    def __init__(self):
        self.device = DivoomTimesGate()
        self.blue_score = 0
        self.red_score = 0
        self.game_time = 0
        self.timer_running = False
        
    def update_display(self):
        """Update the scoreboard display."""
        response = self.device.set_scoreboard_tool(
            self.blue_score, 
            self.red_score
        )
        
        if response and response.get('error_code') == 0:
            print(f"Score: Blue {self.blue_score} - Red {self.red_score}")
            return True
        return False
        
    def add_score(self, team, points=1):
        """Add points to a team's score."""
        if team.lower() == 'blue':
            self.blue_score += points
            # Quick beep for score
            self.device.play_buzzer(50, 0, 50)
        elif team.lower() == 'red':
            self.red_score += points
            # Different beep for red team
            self.device.play_buzzer(75, 0, 75)
        else:
            print(f"Unknown team: {team}")
            return False
            
        return self.update_display()
        
    def reset_scores(self):
        """Reset both scores to zero."""
        self.blue_score = 0
        self.red_score = 0
        return self.update_display()
        
    def start_timer(self, minutes):
        """Start a game timer."""
        print(f"Starting {minutes} minute timer...")
        response = self.device.set_countdown_tool(minutes, 0, 1)
        if response and response.get('error_code') == 0:
            self.timer_running = True
            print("✓ Timer started")
            return True
        return False
        
    def stop_timer(self):
        """Stop the game timer."""
        response = self.device.set_countdown_tool(0, 0, 0)
        if response and response.get('error_code') == 0:
            self.timer_running = False
            print("✓ Timer stopped")
            return True
        return False
        
    def victory_celebration(self, winner):
        """Display victory celebration for the winning team."""
        if winner.lower() == 'blue':
            color = "#0000FF"
            message = "BLUE TEAM WINS!"
        elif winner.lower() == 'red':
            color = "#FF0000"
            message = "RED TEAM WINS!"
        else:
            color = "#FFFF00"
            message = "IT'S A TIE!"
            
        # Victory display
        items = [
            {
                "TextId": 1,
                "type": 22,
                "x": 32,
                "y": 20,
                "dir": 0,
                "font": 3,
                "TextWidth": 64,
                "Textheight": 20,
                "speed": 0,
                "align": 2,
                "TextString": message,
                "color": color
            },
            {
                "TextId": 2,
                "type": 22,
                "x": 32,
                "y": 40,
                "dir": 0,
                "font": 2,
                "TextWidth": 64,
                "Textheight": 16,
                "speed": 0,
                "align": 2,
                "TextString": f"Final: {self.blue_score} - {self.red_score}",
                "color": "#FFFFFF"
            }
        ]
        
        # Play victory sound
        print(f"\n🎉 {message}")
        for _ in range(3):
            self.device.play_buzzer(200, 100, 600)
            time.sleep(0.7)
            
        # Display victory message
        response = self.device.send_display_list(
            lcd_index=3,
            new_flag=1,
            background_gif="",
            item_list=items
        )
        
        return response and response.get('error_code') == 0
        
    def interactive_mode(self):
        """Run the scoreboard in interactive mode."""
        print("\n🎮 Game Scoreboard - Interactive Mode")
        print("=" * 40)
        print("Commands:")
        print("  b/blue [points]  - Add points to blue team")
        print("  r/red [points]   - Add points to red team")
        print("  reset            - Reset scores to 0-0")
        print("  timer <minutes>  - Start countdown timer")
        print("  stop             - Stop timer")
        print("  end              - End game and show winner")
        print("  quit             - Exit scoreboard")
        print("=" * 40)
        
        # Initialize display
        self.update_display()
        
        while True:
            try:
                command = input("\n> ").strip().lower().split()
                
                if not command:
                    continue
                    
                if command[0] in ['q', 'quit', 'exit']:
                    break
                    
                elif command[0] in ['b', 'blue']:
                    points = int(command[1]) if len(command) > 1 else 1
                    self.add_score('blue', points)
                    
                elif command[0] in ['r', 'red']:
                    points = int(command[1]) if len(command) > 1 else 1
                    self.add_score('red', points)
                    
                elif command[0] == 'reset':
                    self.reset_scores()
                    print("Scores reset to 0-0")
                    
                elif command[0] == 'timer' and len(command) > 1:
                    minutes = int(command[1])
                    self.start_timer(minutes)
                    
                elif command[0] == 'stop':
                    self.stop_timer()
                    
                elif command[0] == 'end':
                    if self.blue_score > self.red_score:
                        self.victory_celebration('blue')
                    elif self.red_score > self.blue_score:
                        self.victory_celebration('red')
                    else:
                        self.victory_celebration('tie')
                    break
                    
                else:
                    print("Unknown command. Type 'help' for commands.")
                    
            except ValueError:
                print("Invalid number format")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


def demo_game():
    """Run a demo game with the scoreboard."""
    scoreboard = GameScoreboard()
    
    print("🎮 Starting Demo Game...")
    print("=" * 40)
    
    # Start with 0-0
    scoreboard.update_display()
    time.sleep(1)
    
    # Simulate a game
    game_events = [
        ("Blue team scores!", 'blue', 1),
        ("Red team scores!", 'red', 1),
        ("Blue team scores again!", 'blue', 1),
        ("Red team with a 3-pointer!", 'red', 3),
        ("Blue team catches up!", 'blue', 2),
    ]
    
    for event, team, points in game_events:
        print(f"\n{event}")
        scoreboard.add_score(team, points)
        time.sleep(2)
    
    # End game
    print("\n🏁 Game Over!")
    if scoreboard.blue_score > scoreboard.red_score:
        scoreboard.victory_celebration('blue')
    elif scoreboard.red_score > scoreboard.blue_score:
        scoreboard.victory_celebration('red')
    else:
        scoreboard.victory_celebration('tie')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game Scoreboard for Divoom Times Gate')
    parser.add_argument('--demo', action='store_true', 
                       help='Run a demo game')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_game()
    else:
        # Default to interactive mode
        scoreboard = GameScoreboard()
        scoreboard.interactive_mode() 