import os
import cv2
import datetime

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_blurry(image, threshold=100.0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    return fm < threshold

def is_too_dark(image, threshold=60):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = gray.mean()
    return mean < threshold

def save_capture(raw_img, cropped_img, base_dir='captures'):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    folder = os.path.join(base_dir, now)
    ensure_dir(folder)
    raw_path = os.path.join(folder, 'raw.jpg')
    crop_path = os.path.join(folder, 'cropped.jpg')
    cv2.imwrite(raw_path, raw_img)
    cv2.imwrite(crop_path, cropped_img)
    return {'timestamp': now, 'raw': raw_path, 'cropped': crop_path}
