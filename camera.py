"""
Bare-bones camera system using OpenCV (cv2).

This module provides a simple Camera class that wraps cv2.VideoCapture
and a demo when run as __main__.

Dependencies:
  - opencv-python

Usage example:
    from camera import Camera
    cam = Camera(0)
    if cam.open():
        cam.show()
    cam.release()
"""

import cv2
import time
from typing import Tuple, Optional


class Camera:
    """Simple camera wrapper around cv2.VideoCapture.

    Features:
    - open/release camera
    - read single frames
    - interactive show loop with 'q' to quit and 's' to save a frame
    """

    def __init__(self, src: int = 0, width: Optional[int] = None, height: Optional[int] = None):
        self.src = src
        self.width = width
        self.height = height
        self.cap: Optional[cv2.VideoCapture] = None

    def open(self) -> bool:
        """Open the video capture device.

        Returns True if the device was opened successfully.
        """
        self.cap = cv2.VideoCapture(self.src)
        if not self.cap.isOpened():
            return False

        # Optional: set resolution if requested
        if self.width:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(self.width))
        if self.height:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self.height))
        # small warm-up
        time.sleep(0.1)
        return True

    def read(self) -> Tuple[bool, Optional[any]]:
        """Read a single frame from the camera.

        Returns (ret, frame). If ret is False, frame will be None.
        """
        if self.cap is None:
            return False, None
        ret, frame = self.cap.read()
        if not ret:
            return False, None
        return True, frame

    def release(self) -> None:
        """Release the camera device.
        """
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None
        cv2.destroyAllWindows()

    def show(self, window_name: str = "Camera") -> None:
        """Open a simple preview window. Controls:

        - q: quit
        - s: save current frame as `capture_<timestamp>.png`
        """
        if self.cap is None:
            raise RuntimeError("Camera is not open. Call open() first.")

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        while True:
            ret, frame = self.read()
            if not ret:
                print("Failed to grab frame")
                break

            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                fname = f"capture_{int(time.time())}.png"
                cv2.imwrite(fname, frame)
                print(f"Saved {fname}")

        self.release()


def main():
    cam = Camera(0)
    ok = cam.open()
    if not ok:
        print("Unable to open camera. Is a camera connected and accessible?")
        return
    print("Camera opened. Press 'q' to quit, 's' to save a frame.")
    cam.show()


if __name__ == '__main__':
    main()
