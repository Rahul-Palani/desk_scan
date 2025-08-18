from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import glob
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CAPTURES_DIR = 'captures'

@app.post('/capture')
def capture():
    # Placeholder: actual capture logic should be triggered from main.py or another process
    return {"status": "triggered"}

@app.get('/list')
def list_captures():
    entries = []
    if not os.path.exists(CAPTURES_DIR):
        return []
    for folder in sorted(os.listdir(CAPTURES_DIR), reverse=True):
        folder_path = os.path.join(CAPTURES_DIR, folder)
        if os.path.isdir(folder_path):
            entry = {"id": folder, "raw": None, "cropped": None}
            for f in os.listdir(folder_path):
                if f.startswith('raw'):
                    entry["raw"] = f"/image/{folder}?type=raw"
                if f.startswith('cropped'):
                    entry["cropped"] = f"/image/{folder}?type=cropped"
            entries.append(entry)
    return entries

@app.get('/image/{id}')
def get_image(id: str, type: str = 'raw'):
    folder = os.path.join(CAPTURES_DIR, id)
    if not os.path.exists(folder):
        raise HTTPException(404)
    fname = f'{type}.jpg'
    path = os.path.join(folder, fname)
    if not os.path.exists(path):
        raise HTTPException(404)
    return FileResponse(path)
