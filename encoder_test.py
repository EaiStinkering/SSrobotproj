#!/usr/bin/env python3
"""Quick test to see actual encoder behavior"""
import time
from sparkybotmini import SparkyBotMini

robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)
robot.connect()
robot.set_auto_report(True)
time.sleep(0.5)

print("Initial encoders:")
start = robot.get_encoders()
print(start)

print("\nMoving motor 1 forward for 2 seconds...")
robot.set_motor(50, 0, 0, 0)  # Motor 1 at medium speed
time.sleep(2)

print("Final encoders:")
end = robot.get_encoders()
print(end)

print(f"\nEncoder deltas (counts):")
print(f"  Motor 1: {end[0] - start[0]}")
print(f"  Motor 2: {end[1] - start[1]}")
print(f"  Motor 3: {end[2] - start[2]}")
print(f"  Motor 4: {end[3] - start[3]}")

robot.set_motor(0, 0, 0, 0)
robot.disconnect()
