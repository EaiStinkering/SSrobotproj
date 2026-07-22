#!/usr/bin/env python3
"""SparkyBotMini omnidirectional movement with WASD keyboard controls and arrow key turning"""
#cool movement thingy
import time
import sys
import os
import threading
from sparkybotmini import SparkyBotMini

# Handle keyboard input for non-blocking key detection
try:
    import termios
    import tty
    import select
    
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
    
    def check_key_available():
        rlist, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(rlist)
    
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
    
    def check_key_available():
        return msvcrt.kbhit()

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
print("  W - Forward (hold)")
print("  S - Backward (hold)")
print("  A - Strafe Left (hold)")
print("  D - Strafe Right (hold)")
print("TURNING:")
print("  LEFT ARROW  - Turn Left (hold)")
print("  RIGHT ARROW - Turn Right (hold)")
print("  Q - Quit")
print("-" * 40)

# Start motor update thread
motor_thread = threading.Thread(target=update_motor_speed, daemon=True)
motor_thread.start()

def map_key(key):
    """Map arrow key codes to consistent names"""
    if key == 'D':  # LEFT ARROW on Linux
        return 'left'
    elif key == 'C':  # RIGHT ARROW on Linux
        return 'right'
    return key

try:
    while True:
        # Check if a key is available
        if check_key_available():
            key = get_key()
            key = map_key(key)
            
            if key == 'q':
                print("Stopping robot and exiting...")
                running = False
                robot.set_motor(0, 0, 0, 0)
                break
            elif key in keys_pressed:
                # Key pressed - set to True
                if not keys_pressed[key]:
                    keys_pressed[key] = True
                    print(f"{key.upper()}: ON")
        else:
            # No key available - all keys are released
            for key in keys_pressed:
                if keys_pressed[key]:
                    keys_pressed[key] = False
                    print(f"{key.upper()}: OFF")
        
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
