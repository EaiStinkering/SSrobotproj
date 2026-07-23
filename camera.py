import cv2
import numpy as np

# 1. Initialize the webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Safety check: Ensure the camera was opened correctly
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Target BGR color range based on provided ranges
# Red Range: 0-110, Green Range: 135-255, Blue Range: 0-255
target_bgr_lower = np.array([0, 135, 0])      # Lower bound
target_bgr_upper = np.array([110, 255, 255])  # Upper bound

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

print("Target Detection Active!")
print("Controls:")
print("  'q' - Quit")
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
        # Draw label "corn"
        cv2.putText(frame, "corn", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if center:
            print(f"Target detected at: {center}")
    
    # 3. Display the resulting frame
    cv2.imshow('Webcam Stream - Target Detection', frame)
    cv2.imshow('Target Mask', mask)

    # 4. Handle key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# 5. Release the hardware resource and close all windows
cap.release()
cv2.destroyAllWindows()
