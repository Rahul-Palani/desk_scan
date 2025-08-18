import os
import cv2
import numpy as np
from datetime import datetime

DATA_DIR = "captures"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_blurry(image, threshold=100.0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    return fm < threshold

def is_too_dark(image, threshold=60):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = np.mean(gray)
    return mean < threshold

def save_capture(raw_img, cropped_img, meta=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(DATA_DIR, timestamp)
    ensure_dir(folder)
    raw_path = os.path.join(folder, "raw.jpg")
    crop_path = os.path.join(folder, "cropped.jpg")
    cv2.imwrite(raw_path, raw_img)
    if cropped_img is not None:
        cv2.imwrite(crop_path, cropped_img)
    # Save metadata
    if meta is None:
        meta = {}
    meta_path = os.path.join(folder, "meta.txt")
    with open(meta_path, "w") as f:
        for k, v in meta.items():
            f.write(f"{k}: {v}\n")
    return folder
