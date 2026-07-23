import cv2
import numpy as np

# 1. Initialize the webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Safety check: Ensure the camera was opened correctly
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Target RGB color range (changeable)
# Format: (lower_bound, upper_bound) in BGR (OpenCV uses BGR, not RGB)
# Example: Red target
target_bgr_lower = np.array([0, 0, 100])      # Lower bound for red
target_bgr_upper = np.array([100, 100, 255])  # Upper bound for red

def detect_target(frame, lower, upper):
    """
    Detect pixels within the specified BGR color range.
    Returns: mask (binary image), contours, center of largest contour
    """
    # Convert frame to BGR (already is, but making it explicit)
    # Create a mask for pixels within the color range
    mask = cv2.inRange(frame, lower, upper)
    
    # Apply morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    center = None
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the center of the contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    return mask, contours, center

print("Target Detection Active!")
print("Controls:")
print("  'q' - Quit")
print("  'r' - Change target to Red")
print("  'g' - Change target to Green")
print("  'b' - Change target to Blue")
print("  'y' - Change target to Yellow")
print()

while True:
    # 2. Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Can't receive frame. Exiting stream.")
        break

    # Detect target
    mask, contours, center = detect_target(frame, target_bgr_lower, target_bgr_upper)
    
    # Draw contours and center on the frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    if center:
        cv2.circle(frame, center, 5, (0, 255, 0), -1)
        print(f"Target detected at: {center}")
    
    # 3. Display the resulting frame
    cv2.imshow('Webcam Stream - Target Detection', frame)
    cv2.imshow('Target Mask', mask)

    # 4. Handle key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        # Red target (BGR)
        target_bgr_lower = np.array([0, 0, 100])
        target_bgr_upper = np.array([100, 100, 255])
        print("Target changed to RED")
    elif key == ord('g'):
        # Green target (BGR)
        target_bgr_lower = np.array([0, 100, 0])
        target_bgr_upper = np.array([100, 255, 100])
        print("Target changed to GREEN")
    elif key == ord('b'):
        # Blue target (BGR)
        target_bgr_lower = np.array([100, 0, 0])
        target_bgr_upper = np.array([255, 100, 100])
        print("Target changed to BLUE")
    elif key == ord('y'):
        # Yellow target (BGR)
        target_bgr_lower = np.array([0, 100, 100])
        target_bgr_upper = np.array([100, 255, 255])
        print("Target changed to YELLOW")

# 5. Release the hardware resource and close all windows
cap.release()
cv2.destroyAllWindows()
