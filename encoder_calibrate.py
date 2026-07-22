#!/usr/bin/env python3
"""
Encoder Calibration Script
Run this to determine actual encoder behavior and counts per rotation
"""
import time
from sparkybotmini import SparkyBotMini

def calibrate_encoders():
    robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)
    
    if not robot.connect():
        print("✗ Failed to connect")
        return
    
    robot.set_auto_report(True)
    time.sleep(0.5)
    
    print("=" * 70)
    print("🔧 ENCODER CALIBRATION TEST")
    print("=" * 70)
    
    # Get initial values
    initial = robot.get_encoders()
    print(f"\n📍 Initial encoder values:")
    print(f"   Motor 1: {initial[0]}")
    print(f"   Motor 2: {initial[1]}")
    print(f"   Motor 3: {initial[2]}")
    print(f"   Motor 4: {initial[3]}")
    
    # Run motor 1 only for exactly 10 seconds at speed 50
    print(f"\n▶️  Running Motor 1 at speed 50 for 10 seconds...")
    robot.set_motor(50, 0, 0, 0)
    time.sleep(10)
    robot.set_motor(0, 0, 0, 0)
    
    # Get final values
    final = robot.get_encoders()
    print(f"\n📊 Final encoder values:")
    print(f"   Motor 1: {final[0]}")
    print(f"   Motor 2: {final[1]}")
    print(f"   Motor 3: {final[2]}")
    print(f"   Motor 4: {final[3]}")
    
    # Calculate deltas
    deltas = [final[i] - initial[i] for i in range(4)]
    print(f"\n📈 Encoder DELTAS (10 seconds @ speed 50):")
    print(f"   Motor 1 delta: {deltas[0]}")
    print(f"   Motor 2 delta: {deltas[1]}")
    print(f"   Motor 3 delta: {deltas[2]}")
    print(f"   Motor 4 delta: {deltas[3]}")
    
    print(f"\n💡 KEY FINDINGS:")
    print(f"   - If deltas are ~360: encoder gives 360 counts/rotation")
    print(f"   - If deltas are ~256 or wrap: encoder is likely 8-bit")
    print(f"   - If deltas are ~65535 or wrap: encoder is likely 16-bit")
    print(f"   - If Motor 2,3,4 show ZERO: encoders not connected to those motors")
    
    # Try to detect if encoder is wrapping
    if deltas[0] > 0:
        print(f"\n🔍 Checking for encoder wrapping...")
        if deltas[0] < 100:
            print(f"   ⚠️  LIKELY WRAPPING! Delta too small. Encoders might be rolling over.")
        elif deltas[0] > 10000:
            print(f"   ⚠️  VERY HIGH DELTA! Motor might have multiple rotations.")
        else:
            print(f"   ✓ Delta looks reasonable")
    
    robot.disconnect()
    print("\n" + "=" * 70)

if __name__ == "__main__":
    calibrate_encoders()
