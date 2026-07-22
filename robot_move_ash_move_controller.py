#!/usr/bin/env python3
"""SparkyBotMini omnidirectional movement with WASD keyboard controls and arrow key turning"""
#cool movement thingy
import time
import sys
import os
import threading
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

# Key state tracking
keys_pressed = {
    'w': False,
    'a': False,
    's': False,
    'd': False,
    'left': False,
    'right': False
}

running = True

def update_motor_speed():
    """Calculate and apply motor speeds based on currently pressed keys"""
    while running:
        # Base motor speeds (front-left, front-right, rear-left, rear-right)
        fl = 0
        fr = 0
        rl = 0
        rr = 0
        
        # Handle movement (WASD)
        if keys_pressed['w']:
            # Forward: all motors forward
            fl += motor_speed
            fr += motor_speed
            rl += motor_speed
            rr += motor_speed
        
        if keys_pressed['s']:
            # Backward: all motors backward
            fl -= motor_speed
            fr -= motor_speed
            rl -= motor_speed
            rr -= motor_speed
        
        if keys_pressed['a']:
            # Left strafe: front-left and rear-right backward, front-right and rear-left forward
            fl -= motor_speed
            fr += motor_speed
            rl += motor_speed
            rr -= motor_speed
        
        if keys_pressed['d']:
            # Right strafe: front-left and rear-right forward, front-right and rear-left backward
            fl += motor_speed
            fr -= motor_speed
            rl -= motor_speed
            rr += motor_speed
        
        # Handle turning (arrow keys)
        if keys_pressed['left']:
            # Turn left: counterclockwise rotation
            fl -= turn_speed
            fr += turn_speed
            rl -= turn_speed
            rr += turn_speed
        
        if keys_pressed['right']:
            # Turn right: clockwise rotation
            fl += turn_speed
            fr -= turn_speed
            rl += turn_speed
            rr -= turn_speed
        
        # Apply motor speeds
        robot.set_motor(fl, fr, rl, rr)
        time.sleep(0.05)  # Update at ~20Hz

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

# Start motor update thread
motor_thread = threading.Thread(target=update_motor_speed, daemon=True)
motor_thread.start()

try:
    while True:
        key = get_key()
        
        if key == 'w':
            keys_pressed['w'] = not keys_pressed['w']
            print(f"W: {'ON' if keys_pressed['w'] else 'OFF'}")
        elif key == 's':
            keys_pressed['s'] = not keys_pressed['s']
            print(f"S: {'ON' if keys_pressed['s'] else 'OFF'}")
        elif key == 'a':
            keys_pressed['a'] = not keys_pressed['a']
            print(f"A: {'ON' if keys_pressed['a'] else 'OFF'}")
        elif key == 'd':
            keys_pressed['d'] = not keys_pressed['d']
            print(f"D: {'ON' if keys_pressed['d'] else 'OFF'}")
        elif key == 'D':  # LEFT ARROW on Linux (code 'D')
            keys_pressed['left'] = not keys_pressed['left']
            print(f"LEFT: {'ON' if keys_pressed['left'] else 'OFF'}")
        elif key == 'C':  # RIGHT ARROW on Linux (code 'C')
            keys_pressed['right'] = not keys_pressed['right']
            print(f"RIGHT: {'ON' if keys_pressed['right'] else 'OFF'}")
        elif key == 'left':  # Windows left arrow
            keys_pressed['left'] = not keys_pressed['left']
            print(f"LEFT: {'ON' if keys_pressed['left'] else 'OFF'}")
        elif key == 'right':  # Windows right arrow
            keys_pressed['right'] = not keys_pressed['right']
            print(f"RIGHT: {'ON' if keys_pressed['right'] else 'OFF'}")
        elif key == 'q':
            print("Stopping robot and exiting...")
            running = False
            robot.set_motor(0, 0, 0, 0)
            break
        
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping robot...")
    running = False
    robot.set_motor(0, 0, 0, 0)

finally:
    # Ensure motors are stopped and robot is disconnected
    running = False
    robot.set_motor(0, 0, 0, 0)
    robot.disconnect()
    print("Robot disconnected")
