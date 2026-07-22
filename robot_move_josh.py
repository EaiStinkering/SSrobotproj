#!/usr/bin/env python3
# coding: utf-8
"""
Robot Forward Movement Script
Moves the robot forward 1 meter using encoder feedback with safety features
- Front Left: Motor 1
- Back Left: Motor 2
- Front Right: Motor 3
- Back Right: Motor 4
"""

import time
import signal
import sys
from sparkybotmini import SparkyBotMini

# ===== Configuration =====
WHEEL_DIAMETER_MM = 60  # 60mm omni-wheels
WHEEL_CIRCUMFERENCE_MM = WHEEL_DIAMETER_MM * 3.14159  # π * d
TARGET_DISTANCE_MM = 3000

# Motor speed calibration
MOTOR_SPEED = 10  # Speed value (-100 to 100)

# Encoder counts per wheel rotation
# This depends on the motor encoder PCB - adjust based on your encoder specs
# Typical: 1 PPR (pulse per rotation) = 1 count per motor rotation
# If your encoder gives N counts per rotation, use that value
COUNTS_PER_ROTATION = 360  # Adjust this based on your encoder specifications

# Timeout and safety
MOVEMENT_TIMEOUT = 10  # seconds - max time for movement
ENCODER_READ_TIMEOUT = 0.05  # seconds

# Global E-stop flag
ESTOP_TRIGGERED = False

def estop_handler(signum, frame):
    """Emergency stop handler for Ctrl+C"""
    global ESTOP_TRIGGERED
    ESTOP_TRIGGERED = True
    print("\n🛑 EMERGENCY STOP TRIGGERED!")
    sys.exit(0)

def safe_stop_robot(robot):
    """Safely stop the robot immediately"""
    try:
        robot.set_motor(0, 0, 0, 0)
        print("✓ Motors stopped")
    except Exception as e:
        print(f"✗ Error stopping motors: {e}")

def calculate_encoder_target():
    """Calculate target encoder counts for 1 meter"""
    counts_per_mm = COUNTS_PER_ROTATION / WHEEL_CIRCUMFERENCE_MM
    target_counts = int(TARGET_DISTANCE_MM * counts_per_mm)
    print(f"📊 Target distance: {TARGET_DISTANCE_MM}mm")
    print(f"📊 Counts per rotation: {COUNTS_PER_ROTATION}")
    print(f"📊 Wheel circumference: {WHEEL_CIRCUMFERENCE_MM:.1f}mm")
    print(f"📊 Target encoder counts: {target_counts}")
    return target_counts

def get_average_distance(encoder_deltas):
    """Calculate average distance traveled from encoder deltas"""
    # Average the 4 motor encoder deltas
    avg_encoder = sum(encoder_deltas) / 4
    distance_rotations = avg_encoder / COUNTS_PER_ROTATION
    distance_mm = distance_rotations * WHEEL_CIRCUMFERENCE_MM
    return distance_mm, avg_encoder

def move_forward_1_meter():
    """Main function to move robot forward 1 meter"""
    global ESTOP_TRIGGERED
    
    # Set up E-stop handler
    signal.signal(signal.SIGINT, estop_handler)
    
    print("=" * 60)
    print("🤖 Robot Forward Movement - 1 Meter")
    print("=" * 60)
    
    robot = None
    
    try:
        # Initialize robot
        print("\n🔌 Initializing SparkyBotMini...")
        robot = SparkyBotMini(port="/dev/ttyUSB0", baudrate=115200, debug=False)
        
        # Connect
        if not robot.connect():
            print("✗ Failed to connect to robot!")
            return False
        
        print("✓ Connected to robot")
        time.sleep(0.5)
        
        # Enable auto-reporting for encoder data
        print("📡 Enabling auto-reporting...")
        robot.set_auto_report(True)
        time.sleep(0.5)
        
        # Get initial encoder values
        print("📍 Reading initial encoder positions...")
        initial_encoders = robot.get_encoders()
        print(f"   Motor 1 (FL): {initial_encoders[0]}")
        print(f"   Motor 2 (BL): {initial_encoders[1]}")
        print(f"   Motor 3 (FR): {initial_encoders[2]}")
        print(f"   Motor 4 (BR): {initial_encoders[3]}")
        
        target_counts = calculate_encoder_target()
        
        # Start movement
        print(f"\n▶️  Starting forward movement at speed {MOTOR_SPEED}...")
        print("   (Motor 1=FL, 2=BL, 3=FR, 4=BR)")
        
        robot.set_motor(MOTOR_SPEED, MOTOR_SPEED, MOTOR_SPEED, MOTOR_SPEED)
        
        movement_start_time = time.time()
        last_print_time = movement_start_time
        
        # Movement loop with encoder feedback
        while True:
            # Check E-stop
            if ESTOP_TRIGGERED:
                print("🛑 E-stop detected!")
                safe_stop_robot(robot)
                return False
            
            # Check timeout
            elapsed_time = time.time() - movement_start_time
            if elapsed_time > MOVEMENT_TIMEOUT:
                print(f"✗ Movement timeout ({MOVEMENT_TIMEOUT}s exceeded)!")
                safe_stop_robot(robot)
                return False
            
            # Read current encoder values
            current_encoders = robot.get_encoders()
            
            # Calculate delta from initial position (the fix!)
            encoder_deltas = [current_encoders[i] - initial_encoders[i] for i in range(4)]
            
            # Calculate distance traveled
            distance_mm, avg_counts = get_average_distance(encoder_deltas)
            
            # Print progress every 0.5 seconds
            if time.time() - last_print_time >= 0.5:
                progress_pct = (distance_mm / TARGET_DISTANCE_MM) * 100
                print(f"   [{progress_pct:5.1f}%] Distance: {distance_mm:6.1f}mm | "
                      f"Avg counts: {avg_counts:6.0f} | Time: {elapsed_time:.2f}s")
                last_print_time = time.time()
            
            # Check if target reached
            if distance_mm >= TARGET_DISTANCE_MM:
                print(f"\n✓ Target reached! Distance: {distance_mm:.1f}mm")
                safe_stop_robot(robot)
                time.sleep(0.1)
                break
            
            # Small delay to prevent busy-waiting
            time.sleep(0.01)
        
        # Final encoder readout
        print("\n📊 Final Encoder Values:")
        final_encoders = robot.get_encoders()
        print(f"   Motor 1 (FL): {final_encoders[0]} (delta: {final_encoders[0] - initial_encoders[0]})")
        print(f"   Motor 2 (BL): {final_encoders[1]} (delta: {final_encoders[1] - initial_encoders[1]})")
        print(f"   Motor 3 (FR): {final_encoders[2]} (delta: {final_encoders[2] - initial_encoders[2]})")
        print(f"   Motor 4 (BR): {final_encoders[3]} (delta: {final_encoders[3] - initial_encoders[3]})")
        
        print("\n✓ Movement completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        
        if robot:
            safe_stop_robot(robot)
        
        return False
    
    finally:
        # Cleanup
        if robot:
            try:
                robot.disconnect()
                print("✓ Disconnected from robot")
            except:
                pass
        
        print("=" * 60)

if __name__ == "__main__":
    success = move_forward_1_meter()
    sys.exit(0 if success else 1)
