import cv2
import numpy as np

class Camera:
    def __init__(self, source=0):
        """
        Initialize camera stream.
        source: 0 for default webcam, or RTSP/HTTP stream URL.
        """
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera source: {source}")

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera.")
        return frame

    def release(self):
        self.cap.release()

    def show_stream(self, on_capture_callback=None, hotkey='c'):
        """
        Display video stream. Calls on_capture_callback(frame) when hotkey is pressed.
        hotkey: single character (e.g., 'c' for capture)
        """
        print(f"Press '{hotkey.upper()}' to capture, 'Q' to quit.")
        while True:
            frame = self.read_frame()
            cv2.imshow('DeskCam', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(hotkey):
                if on_capture_callback:
                    on_capture_callback(frame)
            elif key == ord('q'):
                break
        self.release()
        cv2.destroyAllWindows()

import os
from datetime import datetime

if __name__ == "__main__":
    def save_capture(frame):
        os.makedirs("captures", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captures/{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved image to {filename}")

    cam = Camera()
    cam.show_stream(on_capture_callback=save_capture)
