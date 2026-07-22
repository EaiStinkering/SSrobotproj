#!/usr/bin/env python3
"""SparkyBotMini forward movement for 5 seconds"""

import time
from sparkybotmini import SparkyBotMini

# Initialize robot connection
robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)
robot.connect()

# Drive all motors at 50% speed
robot.set_motor(50, 50, 50, 50)
time.sleep(5)

# Stop all motors
robot.set_motor(0, 0, 0, 0)

# Disconnect
robot.disconnect()
