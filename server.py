
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import cv2
import json

app = FastAPI()

# Rotate image endpoint (must be after app is defined)
@app.post("/rotate/{note_id}")
def rotate_image(note_id: str):
    crop_path = os.path.join(DATA_DIR, note_id, "cropped.jpg")
    if not os.path.exists(crop_path):
        raise HTTPException(404, "Cropped image not found")
    img = cv2.imread(crop_path)
    if img is None:
        raise HTTPException(500, "Failed to load image")
    # Rotate 90 degrees clockwise
    rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(crop_path, rotated)
    return {"status": "rotated"}

# Root endpoint for website
@app.get("/")
def root():
    return {"message": "Welcome to the Desk Scanner API. See /docs for API documentation."}
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

# Rename note endpoint
@app.post("/rename/{note_id}")
async def rename_note(note_id: str, request: Request):
    meta_path = os.path.join(DATA_DIR, note_id, "meta.txt")
    if not os.path.exists(meta_path):
        raise HTTPException(404, "Note not found")
    data = await request.json()
    title = data.get("title")
    if not title:
        return JSONResponse({"error": "No title provided"}, status_code=400)
    # Read all meta lines, update or add title
    lines = []
    found = False
    with open(meta_path, "r") as f:
        for line in f:
            if line.startswith("title: "):
                lines.append(f"title: {title}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        lines.append(f"title: {title}\n")
    with open(meta_path, "w") as f:
        f.writelines(lines)
    return {"status": "ok"}
