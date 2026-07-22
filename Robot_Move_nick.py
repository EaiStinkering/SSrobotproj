#!/usr/bin/env python3
"""SparkyBotMini forward movement for 5 seconds with mecanum wheels

Mecanum Wheel Configuration (X-pattern viewed from above):
  - Front Left (m1) & Back Right (m4): One diagonal pair
  - Front Right (m3) & Back Left (m2): Other diagonal pair

Motor Mapping:
  m1 = Front Left
  m2 = Back Left
  m3 = Front Right
  m4 = Back Right

Movement Modes (all motors at same speed):
  - Forward: All motors same direction (+speed)
  - Backward: All motors same direction (-speed)
  - Strafe Left: m1,m3 opposite to m2,m4
  - Strafe Right: m1,m3 opposite to m2,m4
  - Rotate: m1,m2 opposite to m3,m4
"""

import time
from sparkybotmini import SparkyBotMini

# Initialize robot connection
robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)

# Attempt connection
if not robot.connect():
    print("Failed to connect to robot!")
    exit(1)

print("Robot connected. Starting forward movement test...")
print("Moving forward at 50% speed for 5 seconds...")

# For FORWARD movement with mecanum wheels:
# All motors spin in the SAME direction at the SAME speed
# Motor speed range: -100 (full reverse) to +100 (full forward)
robot.set_motor(10, 10, 10, 10)  # 50% forward

# Move for 5 seconds
time.sleep(5)

print("5 seconds complete. Stopping motors...")

# Stop all motors
robot.set_motor(0, 0, 0, 0)

# Disconnect
robot.disconnect()
print("Robot disconnected. Test complete!")
