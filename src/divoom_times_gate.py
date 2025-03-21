import os
import json
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DivoomTimesGate:
    def __init__(self):
        # Get IP address from environment variable or use a default
        self.ip = os.getenv('DIVOOM_TIMES_GATE_IP', '192.168.0.100')  # Default IP if not set
        self.url = f'http://{self.ip}:80/post'

    def send_request(self, command, data):
        """Send a POST request to the Divoom clock."""
        payload = {
            'Command': command,
            **data
        }
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info(f"Successfully sent command: {command}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending command: {command}, Error: {e}")
            return None

    def set_brightness(self, brightness):
        """Set the brightness of the clock."""
        data = {"Brightness": brightness}
        return self.send_request('Channel/SetBrightness', data)

    def get_all_settings(self):
        """Get all settings of the clock."""
        return self.send_request('Channel/GetAllConf', {})

    def set_timezone(self, timezone):
        """Set the time zone of the clock."""
        data = {"TimeZoneValue": timezone}
        return self.send_request('Sys/TimeZone', data)

    def set_weather_location(self, longitude, latitude):
        """Set the location for weather info."""
        data = {"Longitude": str(longitude), "Latitude": str(latitude)}
        return self.send_request('Sys/LogAndLat', data)

    def set_system_time(self, utc):
        """Set the system time for the clock."""
        data = {"Utc": utc}
        return self.send_request('Device/SetUTC', data)

    def switch_screen(self, onoff):
        """Switch the screen on or off."""
        data = {"OnOff": onoff}
        return self.send_request('Channel/OnOffScreen', data)

    def get_device_time(self):
        """Get the device's current system time."""
        return self.send_request('Device/GetDeviceTime', {})

    def set_temperature_mode(self, mode):
        """Set the temperature mode (Celsius or Fahrenheit)."""
        data = {"Mode": mode}
        return self.send_request('Device/SetDisTempMode', data)

    def set_mirror_mode(self, mode):
        """Set the mirror mode."""
        data = {"Mode": mode}
        return self.send_request('Device/SetMirrorMode', data)

    def set_hour_mode(self, mode):
        """Set the hour mode (24-hour or 12-hour)."""
        data = {"Mode": mode}
        return self.send_request('Device/SetTime24Flag', data)

    def get_weather(self):
        """Get the weather information from the device."""
        return self.send_request('Device/GetWeatherInfo', {})

    def get_sub_dial_types(self):
        """Get the available sub dial types."""
        return self.send_request('Channel/GetDialType', {})

    def get_sub_dial_list(self, dial_type, page=1):
        """Get the list of sub dials based on dial type."""
        data = {"DialType": dial_type, "Page": page}
        return self.send_request('Channel/GetDialList', data)

    def get_whole_dial_list(self, page=1):
        """Get the whole dial list."""
        data = {"Page": page}
        return self.send_request('Channel/Get5LcdClockListForCommon', data)

    def select_whole_dial(self, clock_id):
        """Select a whole dial to display."""
        data = {"ClockId": clock_id}
        return self.send_request('Channel/Set5LcdWholeClockId', data)

    def select_channel_type(self, channel_type, lcd_independence=None):
        """Select the channel type (whole dial or independent dial)."""
        data = {"ChannelType": channel_type}
        if lcd_independence:
            data["LcdIndependence"] = lcd_independence
        return self.send_request('Channel/Set5LcdChannelType', data)

    def get_channel_info(self, device_id):
        """Get the channel information of the device."""
        data = {"DeviceId": device_id, "DeviceType": "LCD"}
        return self.send_request('Channel/Get5LcdInfoV2', data)

    def select_sub_dial(self, clock_id, lcd_index, lcd_independence):
        """Select a sub dial to display."""
        data = {"ClockId": clock_id, "LcdIndex": lcd_index, "LcdIndependence": lcd_independence}
        return self.send_request('Channel/SetClockSelectId', data)

    def select_sub_visualizer_channel(self, eq_position, lcd_index, lcd_independence):
        """Select a sub visualizer channel."""
        data = {"EqPosition": eq_position, "LcdIndex": lcd_index, "LcdIndependence": lcd_independence}
        return self.send_request('Channel/SetEqPosition', data)

    def set_countdown_tool(self, minutes, seconds, status):
        """Set the countdown tool on or off."""
        data = {"Minute": minutes, "Second": seconds, "Status": status}
        return self.send_request('Tools/SetTimer', data)

    def set_stopwatch_tool(self, status):
        """Start, stop, or reset the stopwatch."""
        data = {"Status": status}
        return self.send_request('Tools/SetStopWatch', data)

    def set_scoreboard_tool(self, blue_score, red_score):
        """Set the scoreboard for the blue and red teams."""
        data = {"BlueScore": blue_score, "RedScore": red_score}
        return self.send_request('Tools/SetScoreBoard', data)

    def set_noise_tool(self, status):
        """Start or stop the noise tool."""
        data = {"NoiseStatus": status}
        return self.send_request('Tools/SetNoiseStatus', data)

    def play_buzzer(self, active_time, off_time, total_time):
        """Play the buzzer."""
        data = {"ActiveTimeInCycle": active_time, "OffTimeInCycle": off_time, "PlayTotalTime": total_time}
        return self.send_request('Device/PlayBuzzer', data)

    def get_my_like_img_list(self, device_id, device_mac, page=1):
        """Get the list of images liked by the device."""
        data = {"DeviceId": device_id, "DeviceMac": device_mac, "Page": page}
        return self.send_request('Device/GetImgLikeList', data)

    def get_img_upload_list(self, device_id, device_mac, page=1):
        """Get the list of uploaded images."""
        data = {"DeviceId": device_id, "DeviceMac": device_mac, "Page": page}
        return self.send_request('Device/GetImgUploadList', data)

    def play_divoom_gif(self, file_id, lcd_array):
        """Play a Divoom GIF on the clock."""
        data = {"FileId": file_id, "LcdArray": lcd_array}
        return self.send_request('Draw/SendRemote', data)

    def play_gif(self, file_names, lcd_array):
        """Play a GIF on the clock."""
        data = {"FileName": file_names, "LcdArray": lcd_array}
        return self.send_request('Device/PlayGif', data)

    def play_gif_in_all_lcds(self, lcd_files):
        """Play a GIF on all LCDs."""
        data = {f"LCD{i}GifFile": files for i, files in enumerate(lcd_files)}
        return self.send_request('Device/PlayGifLCDs', data)

    def get_font_list(self):
        """Get the list of available fonts."""
        return self.send_request('Device/GetTimeDialFontList', {})

    def send_display_list(self, lcd_index, new_flag, background_gif, item_list):
        """Send a display list to the clock."""
        data = {"LcdIndex": lcd_index, "NewFlag": new_flag, "BackgroudGif": background_gif, "ItemList": item_list}
        return self.send_request('Draw/SendHttpItemList', data)

    def send_animation(self, pic_num, pic_width, pic_offset, pic_id, pic_speed, pic_data, lcd_array):
        """Send animation frames to the clock."""
        data = {"PicNum": pic_num, "PicWidth": pic_width, "PicOffset": pic_offset, "PicID": pic_id,
                "PicSpeed": pic_speed, "PicData": pic_data, "LcdArray": lcd_array}
        return self.send_request('Draw/SendHttpGif', data)

    def send_text(self, lcd_index, text_id, x, y, dir, font, text_width, text_string, speed, color, align):
        """Send text to be displayed on the clock."""
        data = {"LcdIndex": lcd_index, "TextId": text_id, "x": x, "y": y, "dir": dir, "font": font,
                "TextWidth": text_width, "TextString": text_string, "speed": speed, "color": color, "align": align}
        return self.send_request('Draw/SendHttpText', data)

    def command_list(self, command_list):
        """Send a list of commands to the clock."""
        data = {"CommandList": command_list}
        return self.send_request('Draw/CommandList', data)

    def url_command_file(self, command_url):
        """Use an HTTP command source from a URL."""
        data = {"CommandUrl": command_url}
        return self.send_request('Draw/UseHTTPCommandSource', data)

# Example usage:
if __name__ == "__main__":
    divoom = DivoomTimesGate()
    response = divoom.set_brightness(80)
    if response:
        logging.info(f"Response: {response}")

