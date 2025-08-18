from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
DATA_DIR = "captures"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/list")
def list_captures():
    if not os.path.exists(DATA_DIR):
        return []
    folders = sorted(os.listdir(DATA_DIR), reverse=True)
    results = []
    for folder in folders:
        meta_path = os.path.join(DATA_DIR, folder, "meta.txt")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = dict(line.strip().split(": ", 1) for line in f if ": " in line)
        else:
            meta = {}
        results.append({"id": folder, "meta": meta})
    return results

@app.get("/image/{capture_id}/{img_type}")
def get_image(capture_id: str, img_type: str):
    if img_type not in ("raw", "cropped"):
        raise HTTPException(400, "img_type must be 'raw' or 'cropped'")
    img_path = os.path.join(DATA_DIR, capture_id, f"{img_type}.jpg")
    if not os.path.exists(img_path):
        raise HTTPException(404, "Image not found")
    return FileResponse(img_path)

@app.post("/capture")
def trigger_capture():
    # This is a stub; actual capture should be triggered from main.py
    return {"status": "Not implemented in backend. Use the main app to capture."}
