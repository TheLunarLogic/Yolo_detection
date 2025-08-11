from ultralytics import YOLO
import cv2
import time
import geocoder
from db_utils import init_db, insert_detection

model = YOLO("yolo11n.pt")  
init_db()

# Flag to control loop
capture_running = False

def get_gps():
    g = geocoder.ip('me')
    return {"lat": g.latlng[0], "lon": g.latlng[1]}

def run_detection():
    global capture_running
    cap = cv2.VideoCapture(0)

    while capture_running:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, classes=[0])
        person_count = len(results[0].boxes.cls)

        if person_count > 0:
            gps = get_gps()
            current_time = time.strftime("%H:%M:%S", time.localtime())
            insert_detection(person_count, current_time, gps["lat"], gps["lon"])
            print({
                "person_count": person_count,
                "time": current_time,
                "lat": gps["lat"],
                "lon": gps["lon"]
            })

    cap.release()

def start_detection():
    global capture_running
    capture_running = True
    run_detection()

def stop_detection():
    global capture_running
    capture_running = False
