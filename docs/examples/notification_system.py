#!/usr/bin/env python3
"""
Notification System Example

This example shows how to create a notification system that:
- Displays important messages
- Uses the buzzer for alerts
- Shows different types of notifications
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from divoom_times_gate import DivoomTimesGate


class NotificationSystem:
    """A simple notification system for Divoom Times Gate."""
    
    def __init__(self):
        self.device = DivoomTimesGate()
        
    def send_notification(self, message, notification_type="info", duration=5):
        """
        Send a notification to the device.
        
        Args:
            message: The notification message
            notification_type: Type of notification (info, warning, error, success)
            duration: How long to display the notification
        """
        # Define colors for different notification types
        colors = {
            "info": "#0080FF",     # Blue
            "warning": "#FFA500",  # Orange
            "error": "#FF0000",    # Red
            "success": "#00FF00"   # Green
        }
        
        # Define buzzer patterns for different types
        buzzer_patterns = {
            "info": (100, 0, 100),      # Single short beep
            "warning": (200, 100, 500),  # Two medium beeps
            "error": (300, 100, 700),    # Three longer beeps
            "success": (150, 50, 350)    # Two quick beeps
        }
        
        color = colors.get(notification_type, "#FFFFFF")
        buzzer = buzzer_patterns.get(notification_type, (100, 0, 100))
        
        # Create notification display
        items = [
            # Notification type icon/text at top
            {
                "TextId": 1,
                "type": 22,
                "x": 32,
                "y": 5,
                "dir": 0,
                "font": 2,
                "TextWidth": 64,
                "Textheight": 12,
                "speed": 0,
                "align": 2,
                "TextString": notification_type.upper(),
                "color": color
            },
            # Main message
            {
                "TextId": 2,
                "type": 22,
                "x": 32,
                "y": 25,
                "dir": 0,
                "font": 3,
                "TextWidth": 60,
                "Textheight": 20,
                "speed": 30 if len(message) > 10 else 0,
                "align": 2,
                "TextString": message,
                "color": "#FFFFFF"
            },
            # Timestamp at bottom
            {
                "TextId": 3,
                "type": 23,
                "x": 32,
                "y": 50,
                "dir": 0,
                "font": 1,
                "TextWidth": 64,
                "Textheight": 10,
                "speed": 0,
                "update_time": 60,
                "align": 2,
                "TextString": "http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0",
                "color": "#808080"  # Gray
            }
        ]
        
        # Play buzzer alert
        print(f"🔔 Sending {notification_type} notification: {message}")
        self.device.play_buzzer(*buzzer)
        
        # Display notification
        response = self.device.send_display_list(
            lcd_index=3,  # Center panel
            new_flag=1,
            background_gif="",
            item_list=items
        )
        
        if response and response.get('error_code') == 0:
            print("✓ Notification sent successfully")
            
            # Keep notification displayed for specified duration
            if duration > 0:
                time.sleep(duration)
                # You might want to restore previous display here
                
        else:
            print("✗ Failed to send notification")
            
    def demo_notifications(self):
        """Demonstrate different types of notifications."""
        notifications = [
            ("Meeting in 5 minutes", "info", 3),
            ("Low battery: 20%", "warning", 3),
            ("Connection failed", "error", 3),
            ("Task completed!", "success", 3)
        ]
        
        for message, ntype, duration in notifications:
            self.send_notification(message, ntype, duration)
            time.sleep(1)  # Brief pause between notifications


if __name__ == "__main__":
    # Create notification system
    notifier = NotificationSystem()
    
    # Run demo
    print("Starting notification demo...")
    notifier.demo_notifications()
    
    # Example of a single notification
    print("\nSending a custom notification...")
    notifier.send_notification("Hello from Python!", "success", 5)