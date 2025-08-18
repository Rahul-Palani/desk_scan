import sys
import os
import threading
from camera import Camera
from page_detect import find_largest_quad, four_point_transform
from storage import save_capture, is_blurry, is_too_dark

# --- Hotkey support (cross-platform) ---
try:
    import keyboard  # pip install keyboard
except ImportError:
    keyboard = None
    print("[WARN] 'keyboard' module not found. Manual capture hotkey will not work.")


def capture_and_save(frame):
    quad = find_largest_quad(frame)
    if quad is None:
        print("No page detected. Skipping.")
        return
    cropped = four_point_transform(frame, quad)
    if is_blurry(cropped):
        print("Image too blurry. Skipping.")
        return
    if is_too_dark(cropped):
        print("Image too dark. Skipping.")
        return
    info = save_capture(frame, cropped)
    print(f"Saved: {info}")


def main():
    # Use 0 for webcam, or provide RTSP/HTTP stream URL for iPhone (e.g., via EpocCam, Camo, or similar)
    cam_source = 0  # Change to your iPhone stream URL if needed
    cam = Camera(source=cam_source)

    def on_capture(frame):
        capture_and_save(frame)

    if keyboard:
        def hotkey_listener():
            print("[Hotkey] Press Ctrl+Shift+C to capture, Esc to quit.")
            keyboard.add_hotkey('ctrl+shift+c', lambda: on_capture(cam.read_frame()))
            keyboard.wait('esc')
            os._exit(0)
        threading.Thread(target=hotkey_listener, daemon=True).start()

    cam.show_stream(on_capture_callback=on_capture, hotkey='c')

if __name__ == '__main__':
    main()
