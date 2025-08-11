from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
import sqlite3
import threading
import json
import yolo_detect

DB_NAME = "detections.db"
app = FastAPI()

class Detection(BaseModel):
    id: int
    person_count: int
    time: str
    lat: float
    lon: float

def read_detections_from_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM detections")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/detections", response_model=List[Detection])
def get_detections():
    rows = read_detections_from_db()
    detections = [
        Detection(id=row[0], person_count=row[1], time=row[2], lat=row[3], lon=row[4]).dict()
        for row in rows
    ]
    return JSONResponse(content=detections)

@app.post("/start-yolo")
def start_yolo():
    if yolo_detect.capture_running:
        return {"status": "YOLO already running"}
    thread = threading.Thread(target=yolo_detect.start_detection, daemon=True)
    thread.start()
    return {"status": "YOLO started"}

@app.post("/stop-yolo")
def stop_yolo():
    if not yolo_detect.capture_running:
        return {"status": "YOLO is not running"}
    yolo_detect.stop_detection()
    return {"status": "YOLO stopped"}
