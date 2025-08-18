import sys
import os
import threading
from camera import Camera
from page_detect import detect_page
from storage import save_capture, is_blurry, is_too_dark

# --- Hotkey support (cross-platform) ---
try:
    import keyboard  # pip install keyboard
except ImportError:
    keyboard = None
    print("[WARN] 'keyboard' module not found. Manual capture hotkey will not work.")


def capture_and_save(frame):
    print("Captured frame. Detecting page...")
    cropped, contour = detect_page(frame)
    if cropped is None:
        print("No page detected. Skipping save.")
        return
    # Skip if cropped image is too small (likely a keyboard or not a page)
    h, w = cropped.shape[:2]
    if h < 200 or w < 200:
        print(f"Detected region too small (h={h}, w={w}). Skipping save.")
        return
    if is_blurry(cropped):
        print("Image is too blurry. Skipping save.")
        return
    if is_too_dark(cropped):
        print("Image is too dark. Skipping save.")
        return
    meta = {"note": "Manual capture"}
    folder = save_capture(frame, cropped, meta)
    print(f"Saved to {folder}")


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
