import cv2

# 1. Initialize the webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Safety check: Ensure the camera was opened correctly
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

while True:
    # 2. Capture frame-by-frame
    # 'ret' is a boolean (True if frame read correctly), 'frame' is the image array
    ret, frame = cap.read()

    if not ret:
        print("Error: Can't receive frame. Exiting stream.")
        break

    # 3. Display the resulting frame in a window named 'Webcam Stream'
    cv2.imshow('Webcam Stream', frame)

    # 4. Break the loop if the 'q' key is pressed
    # cv2.waitKey(1) waits 1 millisecond for a key event
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Release the hardware resource and close all windows
cap.release()
cv2.destroyAllWindows()
