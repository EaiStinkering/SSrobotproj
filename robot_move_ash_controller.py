#!/usr/bin/env python3
"""SparkyBotMini omnidirectional movement with WASD keyboard controls and arrow key turning"""
#cool movement thingy
import time
import sys
import os
from sparkybotmini import SparkyBotMini

# Handle keyboard input
try:
    import termios
    import tty
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            # Handle arrow keys
            if ch == '\x1b':  # Escape sequence
                sys.stdin.read(1)  # Read '['
                arrow_key = sys.stdin.read(1)
                return arrow_key
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
except ImportError:
    # Fallback for Windows
    import msvcrt
    def get_key():
        key = msvcrt.getch()
        if key == b'\xe0':  # Arrow key prefix on Windows
            arrow_key = msvcrt.getch()
            if arrow_key == b'K':
                return 'left'
            elif arrow_key == b'M':
                return 'right'
        return key.decode('utf-8').lower()

# Initialize robot connection
robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)
robot.connect()

motor_speed = 50  # Speed percentage (0-100)
turn_speed = 50   # Turn speed percentage (0-100)

print("Robot movement control")
print("-" * 40)
print("MOVEMENT:")
print("  W - Forward")
print("  S - Backward")
print("  A - Strafe Left")
print("  D - Strafe Right")
print("TURNING:")
print("  LEFT ARROW  - Turn Left (counterclockwise)")
print("  RIGHT ARROW - Turn Right (clockwise)")
print("  Q - Quit")
print("-" * 40)

try:
    while True:
        key = get_key()
        
        if key == 'w':
            # Forward: all motors forward
            print("Moving FORWARD")
            robot.set_motor(motor_speed, motor_speed, motor_speed, motor_speed)
        
        elif key == 's':
            # Backward: all motors backward
            print("Moving BACKWARD")
            robot.set_motor(-motor_speed, -motor_speed, -motor_speed, -motor_speed)
        
        elif key == 'a':
            # Left: omni wheels strafe left
            # Front-left and rear-right forward, front-right and rear-left backward
            print("Moving LEFT")
            robot.set_motor(-motor_speed, motor_speed, motor_speed, -motor_speed)
        
        elif key == 'd':
            # Right: omni wheels strafe right
            # Front-right and rear-left forward, front-left and rear-right backward
            print("Moving RIGHT")
            robot.set_motor(motor_speed, -motor_speed, -motor_speed, motor_speed)
        
        elif key == 'D':  # LEFT ARROW on Linux (code 'D')
            # Turn left: counterclockwise rotation
            # Left side motors backward, right side motors forward
            print("Turning LEFT (counterclockwise)")
            robot.set_motor(-turn_speed, -turn_speed, turn_speed, turn_speed)
        
        elif key == 'C':  # RIGHT ARROW on Linux (code 'C')
            # Turn right: clockwise rotation
            # Left side motors forward, right side motors backward
            print("Turning RIGHT (clockwise)")
            robot.set_motor(turn_speed, turn_speed, -turn_speed, -turn_speed)
        
        elif key == 'left':  # Windows left arrow
            print("Turning LEFT (counterclockwise)")
            robot.set_motor(-turn_speed, -turn_speed, turn_speed, turn_speed)
        
        elif key == 'right':  # Windows right arrow
            print("Turning RIGHT (clockwise)")
            robot.set_motor(turn_speed, turn_speed, -turn_speed, -turn_speed)
        
        elif key == 'q':
            print("Stopping robot and exiting...")
            robot.set_motor(0, 0, 0, 0)
            break
        
        else:
            # Stop on unknown key
            robot.set_motor(0, 0, 0, 0)

except KeyboardInterrupt:
    print("\nStopping robot...")
    robot.set_motor(0, 0, 0, 0)

finally:
    # Ensure motors are stopped and robot is disconnected
    robot.set_motor(0, 0, 0, 0)
    robot.disconnect()
    print("Robot disconnected")
