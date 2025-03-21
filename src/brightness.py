import time
from divoom_times_gate import DivoomTimesGate  # Assuming the class is saved in divoom_times_gate.py

# Create an instance of the DivoomTimesGate class
divoom = DivoomTimesGate()

# Set the brightness to 50%
response = divoom.set_brightness(50)
if response:
    print(f"Brightness set to 50%: {response}")
else:
    print("Failed to set brightness to 50%")

# Wait for 10 seconds
time.sleep(10)

# Set the brightness to 100%
response = divoom.set_brightness(100)
if response:
    print(f"Brightness set to 100%: {response}")
else:
    print("Failed to set brightness to 100%")

