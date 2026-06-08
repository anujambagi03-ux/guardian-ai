from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Vehicle, Violation, Accident
from schemas import VehicleCreate, ViolationCreate, AccidentCreate

from video_processor import extract_frames
from vehicle_detector import detect_vehicles
from vehicle_db import save_detected_vehicles

from violation_detector import detect_violations
from violation_db import save_detected_violations

import os
import shutil

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Guardian AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "project": "Guardian AI",
        "status": "Backend Running"
    }


@app.get("/health")
def health():
    return {
        "message": "System Healthy"
    }


@app.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):
    total_vehicles = db.query(Vehicle).count()
    detected_violations = db.query(Violation).count()
    accident_alerts = db.query(Accident).count()

    return {
        "total_vehicles": total_vehicles,
        "detected_violations": detected_violations,
        "accident_alerts": accident_alerts
    }


@app.get("/dashboard/details")
def dashboard_details(
    db: Session = Depends(get_db)
):
    vehicles = db.query(Vehicle).order_by(
        Vehicle.id.desc()
    ).limit(10).all()

    violations = db.query(Violation).order_by(
        Violation.id.desc()
    ).limit(10).all()

    accidents = db.query(Accident).order_by(
        Accident.id.desc()
    ).limit(10).all()

    recent_vehicles = []
    recent_violations = []
    recent_accidents = []

    for vehicle in vehicles:
        recent_vehicles.append({
            "id": vehicle.id,
            "vehicle_number": vehicle.vehicle_number,
            "vehicle_type": vehicle.vehicle_type,
            "detection_time": str(vehicle.detection_time)
        })

    for violation in violations:
        recent_violations.append({
            "id": violation.id,
            "vehicle_number": violation.vehicle_number,
            "violation_type": violation.violation_type,
            "location": violation.location,
            "timestamp": str(violation.timestamp)
        })

    for accident in accidents:
        recent_accidents.append({
            "id": accident.id,
            "location": accident.location,
            "severity": accident.severity,
            "timestamp": str(accident.timestamp)
        })

    return {
        "recent_vehicles": recent_vehicles,
        "recent_violations": recent_violations,
        "recent_accidents": recent_accidents
    }


@app.get("/test")
def test():
    return {
        "message": "working"
    }


# =====================================================
# VIDEO UPLOAD + FRAME EXTRACTION + YOLO + DATABASE
# =====================================================

@app.post("/upload-video")
def upload_video(
    file: UploadFile = File(...)
):
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    frame_analysis = extract_frames(
        file_path
    )

    vehicle_analysis = detect_vehicles()

    save_detected_vehicles(
    vehicle_analysis
    )

    violation_analysis = detect_violations(
    vehicle_analysis
    )

    save_detected_violations(
    violation_analysis
   )

    
        
    

    return {
    "message": "Video uploaded successfully",
    "filename": file.filename,
    "path": file_path,
    "frame_analysis": frame_analysis,
    "vehicle_analysis": vehicle_analysis,
    "violation_analysis": violation_analysis
    }

# =====================================================
# VEHICLES
# =====================================================

@app.post("/vehicles")
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db)
):
    new_vehicle = Vehicle(
        vehicle_number=vehicle.vehicle_number,
        vehicle_type=vehicle.vehicle_type
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return {
        "id": new_vehicle.id,
        "vehicle_number": new_vehicle.vehicle_number,
        "vehicle_type": new_vehicle.vehicle_type
    }


@app.get("/vehicles")
def get_all_vehicles(
    db: Session = Depends(get_db)
):
    vehicles = db.query(Vehicle).all()

    result = []

    for vehicle in vehicles:
        result.append({
            "id": vehicle.id,
            "vehicle_number": vehicle.vehicle_number,
            "vehicle_type": vehicle.vehicle_type,
            "detection_time": str(vehicle.detection_time)
        })

    return result


# =====================================================
# VIOLATIONS
# =====================================================

@app.post("/violations")
def create_violation(
    violation: ViolationCreate,
    db: Session = Depends(get_db)
):
    new_violation = Violation(
        vehicle_number=violation.vehicle_number,
        violation_type=violation.violation_type,
        location=violation.location
    )

    db.add(new_violation)
    db.commit()
    db.refresh(new_violation)

    return new_violation


@app.get("/violations")
def get_all_violations(
    db: Session = Depends(get_db)
):
    violations = db.query(Violation).all()

    result = []

    for violation in violations:
        result.append({
            "id": violation.id,
            "vehicle_number": violation.vehicle_number,
            "violation_type": violation.violation_type,
            "location": violation.location,
            "timestamp": str(violation.timestamp)
        })

    return result


# =====================================================
# ACCIDENTS
# =====================================================

@app.post("/accidents")
def create_accident(
    accident: AccidentCreate,
    db: Session = Depends(get_db)
):
    new_accident = Accident(
        location=accident.location,
        severity=accident.severity
    )

    db.add(new_accident)
    db.commit()
    db.refresh(new_accident)

    return new_accident


@app.get("/accidents")
def get_all_accidents(
    db: Session = Depends(get_db)
):
    accidents = db.query(Accident).all()

    result = []

    for accident in accidents:
        result.append({
            "id": accident.id,
            "location": accident.location,
            "severity": accident.severity,
            "timestamp": str(accident.timestamp)
        })

    return result