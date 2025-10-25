desk_scan

A macOS-based scanner utility using Continuity Camera and Python + OpenCV. Capture a paper document from your desk, detect its edges, and send the processed result to a frontend interface.

Overview

This project provides a lightweight alternative to traditional document scanners. By leveraging macOS Continuity Camera, it captures images directly from an iPhone or iPad and processes them using OpenCV to detect and crop the document. The final output is served to a simple frontend for viewing or download.

Key Features

-Uses macOS Continuity Camera for image capture
-Performs edge detection and perspective correction with OpenCV
-Automatically crops desk documents
-Python-based backend service
-Frontend interface for preview and interaction

How It Works

-The frontend triggers a request to the Python backend
-The backend opens Continuity Camera for image capture
-OpenCV detects document edges and applies a perspective transform
-The processed image is stored and returned to the frontend

Installation

Clone the repository:

git clone https://github.com/Rahul-Palani/desk_scan.git
cd desk_scan

Install dependencies:

pip install -r requirements.txt

Ensure macOS Continuity Camera is enabled and paired with your iPhone or iPad.

Usage

Start the backend server:
python server.py
Open frontend/index.html in your browser
Trigger a capture to scan a document
The processed image will be shown after edge detection and cropping

Project Structure
desk_scan/
├─ .vscode/               # Editor configuration
├─ captures/              # Stored raw and processed images
├─ frontend/              # Web UI files (HTML, CSS, JS)
├─ camera.py              # Handles Continuity Camera capture
├─ page_detect.py         # Edge detection and perspective transform logic
├─ storage.py             # File storage utilities
├─ server.py              # Python backend (Flask or similar)
├─ main.py                # Optional entry script
├─ requirements.txt       # Dependencies
└─ HOW_TO_RUN.txt         # Additional run instructions

Requirements

-macOS with Continuity Camera support 
-iPhone or iPad connected via Continuity Camera
-Python 3.x

Future Enhancements
Add PDF export and multi-page scanning
Implement image enhancement (contrast, brightness)
Provide mobile-responsive frontend
Include cloud storage integration (Google Drive, iCloud)
Contributing

Fork the repository

Create a feature or fix branch

Submit a pull request with a meaningful description

License

Specify the project license here (e.g., MIT, Apache 2.0)

Contact

Created by Rahul Palani

For inquiries or suggestions, please open an issue or reach out via GitHub
