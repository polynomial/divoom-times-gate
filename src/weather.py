from divoom_times_gate import DivoomTimesGate

# Create an instance of the DivoomTimesGate class
divoom = DivoomTimesGate()

# Get the weather information
response = divoom.get_weather()
if response:
    print(f"Weather information: {response}")
else:
    print("Failed to get weather information") 