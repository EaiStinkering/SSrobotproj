import cv2
import numpy as np
from robot_move_real_ash import robo_movement

# ===== COLOR RANGE CONFIGURATION =====
# Adjust these values to detect different colors
# BGR format (Blue, Green, Red) - values range from 0-255
# 
# Examples:
#   Green: lower=[35, 40, 40], upper=[90, 255, 255]
#   Blue:  lower=[100, 0, 0], upper=[255, 100, 100]
#   Red:   lower=[0, 0, 100], upper=[100, 100, 255]
#
# Red/Yellow Range (Corn):
RED_LOWER = 0
RED_UPPER = 97.78
GREEN_LOWER = 108.89
GREEN_UPPER = 212.22
BLUE_LOWER = 19.44
BLUE_UPPER = 130

# Build color range arrays from variables
target_bgr_lower = np.array([BLUE_LOWER, GREEN_LOWER, RED_LOWER])
target_bgr_upper = np.array([BLUE_UPPER, GREEN_UPPER, RED_UPPER])

# ===== TARGET LABEL =====
TARGET_LABEL = "corn"

# ===== FRAMERATE CONFIGURATION =====
# Set desired framerate in FPS (frames per second)
# Calculation: delay_ms = 1000 / FPS
# Examples: 5 FPS = 200ms, 10 FPS = 100ms, 30 FPS = 33ms
TARGET_FPS = 5
FRAME_DELAY_MS = int(1000 / TARGET_FPS)

# ===== RESOLUTION CONFIGURATION =====
# Set desired resolution (width, height)
# Lower resolution = faster processing
# Examples: 
#   320x240 (QVGA) - very low
#   640x480 (VGA) - standard
#   1280x720 (HD) - high
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# 1. Initialize the webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Safety check: Ensure the camera was opened correctly
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

def detect_target(frame, lower, upper):
    """
    Detect pixels within the specified BGR color range.
    Returns: mask (binary image), bounding box, center
    """
    # Create a mask for pixels within the color range
    mask = cv2.inRange(frame, lower, upper)
    
    # Apply morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bbox = None
    center = None
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        # Get bounding box for the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        bbox = (x, y, w, h)
        # Calculate the center of the bounding box
        center = (x + w // 2, y + h // 2)
    
    return mask, bbox, center

def move_towards_target(center, frame_width, frame_height):
    """
    Determine movement direction based on target position in frame.
    Center of frame is (frame_width/2, frame_height/2)
    """
    center_x = frame_width / 2
    center_y = frame_height / 2
    
    target_x, target_y = center
    
    # Tolerance for center (pixels)
    tolerance = 30
    
    # Horizontal movement
    if target_x < center_x - tolerance:
        # Target is on the left, strafe left
        robo_movement("a")
        print("Moving LEFT to track target")
    elif target_x > center_x + tolerance:
        # Target is on the right, strafe right
        robo_movement("d")
        print("Moving RIGHT to track target")
    
    # Vertical movement (forward/backward)
    if target_y < center_y - tolerance:
        # Target is in upper half, move forward
        robo_movement("w")
        print("Moving FORWARD to track target")
    elif target_y > center_y + tolerance:
        # Target is in lower half, move backward
        robo_movement("s")
        print("Moving BACKWARD to track target")
    
    # If target is centered, stop
    if (abs(target_x - center_x) <= tolerance and 
        abs(target_y - center_y) <= tolerance):
        robo_movement("s")  # Stop movement
        print("Target CENTERED - stopping")

print("Target Detection Active with Robot Movement!")
print("Controls:")
print("  'q' - Quit")
print(f"Detecting: {TARGET_LABEL}")
print(f"Color Range (BGR): R({RED_LOWER}-{RED_UPPER}), G({GREEN_LOWER}-{GREEN_UPPER}), B({BLUE_LOWER}-{BLUE_UPPER})")
print(f"Framerate: {TARGET_FPS} FPS ({FRAME_DELAY_MS}ms delay)")
print(f"Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
print()

while True:
    # 2. Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Can't receive frame. Exiting stream.")
        break

    # Detect target
    mask, bbox, center = detect_target(frame, target_bgr_lower, target_bgr_upper)
    
    # Draw bounding box and label on the frame
    if bbox:
        x, y, w, h = bbox
        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Draw label
        cv2.putText(frame, TARGET_LABEL, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if center:
            print(f"Target detected at: {center}")
            # Call movement function to track target
            move_towards_target(center, FRAME_WIDTH, FRAME_HEIGHT)
    else:
        # No target detected, stop robot
        robo_movement("no_corn")
    
    # 3. Display the resulting frame
    cv2.imshow('Webcam Stream - Target Detection', frame)
    cv2.imshow('Target Mask', mask)

    # 4. Handle key presses
    key = cv2.waitKey(FRAME_DELAY_MS) & 0xFF
    if key == ord('q'):
        break

# 5. Release the hardware resource and close all windows
robo_movement("x")  # Stop robot before exit
cap.release()
cv2.destroyAllWindows()
