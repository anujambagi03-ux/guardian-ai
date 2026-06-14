from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from traffic_flow_service import (
    generate_traffic_flow
)
from near_miss_service import (
    generate_near_miss_event,
    get_near_miss_events,
    get_near_miss_analytics
)

from models import (
    Base,
    Vehicle,
    Violation,
    Accident,
    Alert,
    TrafficFlow,
    DetectionFrame,
    NearMissEvent
)

from schemas import (
    VehicleCreate,
    ViolationCreate,
    AccidentCreate,
    AlertCreate
)

from video_processor import extract_frames
from vehicle_detector import detect_vehicles
from vehicle_db import save_detected_vehicles

from violation_detector import detect_violations
from violation_db import save_detected_violations

from accident_detector import detect_accidents
from accident_db import save_detected_accidents

from analytics_service import generate_analytics

from report_service import (
    vehicle_report,
    violation_report,
    accident_report,
    summary_report
)

from risk_predictor import predict_accident_risk

from alert_service import (
    create_alert,
    get_all_alerts,
    get_alert_by_id,
    delete_alert
)

from cv_service import (
    get_cv_status,
    simulate_detection,
    get_detections,
    get_cv_analytics,
    save_real_detection
)

from tracking_service import (
    create_tracking_records,
    get_tracking_data
)

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
    total_alerts = db.query(Alert).count()

    return {
        "total_vehicles": total_vehicles,
        "detected_violations": detected_violations,
        "accident_alerts": accident_alerts,
        "total_alerts": total_alerts
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

    alerts = db.query(Alert).order_by(
        Alert.id.desc()
    ).limit(10).all()

    recent_vehicles = []
    recent_violations = []
    recent_accidents = []
    recent_alerts = []

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

    for alert in alerts:
        recent_alerts.append({
            "id": alert.id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "status": alert.status,
            "created_at": str(alert.created_at)
        })

    return {
        "recent_vehicles": recent_vehicles,
        "recent_violations": recent_violations,
        "recent_accidents": recent_accidents,
        "recent_alerts": recent_alerts
    }


# =====================================================
# ANALYTICS
# =====================================================

@app.get("/analytics")
def analytics(
    db: Session = Depends(get_db)
):
    return generate_analytics(db)

# =====================================================
# REAL TIME MONITORING
# =====================================================

@app.get("/monitoring/live")
def monitoring_live(
    db: Session = Depends(get_db)
):
    from datetime import datetime

    total_vehicles = db.query(
        Vehicle
    ).count()

    total_violations = db.query(
        Violation
    ).count()

    total_accidents = db.query(
        Accident
    ).count()

    total_alerts = db.query(
        Alert
    ).count()

    risk_status = (
        "HIGH"
        if total_alerts > 0
        else "LOW"
    )

    return {
        "total_vehicles": total_vehicles,
        "total_violations": total_violations,
        "total_accidents": total_accidents,
        "total_alerts": total_alerts,
        "risk_status": risk_status,
        "last_updated": str(
            datetime.utcnow()
        )
    }
# =====================================================
# REPORTS
# =====================================================

@app.get("/reports/vehicles")
def vehicles_report(
    db: Session = Depends(get_db)
):
    return vehicle_report(db)


@app.get("/reports/violations")
def violations_report(
    db: Session = Depends(get_db)
):
    return violation_report(db)


@app.get("/reports/accidents")
def accidents_report(
    db: Session = Depends(get_db)
):
    return accident_report(db)


@app.get("/reports/summary")
def reports_summary(
    db: Session = Depends(get_db)
):
    return summary_report(db)


@app.get("/test")
def test():
    return {
        "message": "working"
    }


# =====================================================
# VIDEO UPLOAD + AI PIPELINE
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

    db = SessionLocal()

    save_real_detection(
        db,
        vehicle_analysis
    )

   

    create_tracking_records(
    db,
    vehicle_analysis
   )


    db.close()

    violation_analysis = detect_violations(
        vehicle_analysis
    )

    save_detected_violations(
        violation_analysis
    )

    accident_analysis = detect_accidents(
        violation_analysis
    )

    save_detected_accidents(
        accident_analysis
    )

    return {
        "message": "Video uploaded successfully",
        "filename": file.filename,
        "path": file_path,
        "frame_analysis": frame_analysis,
        "vehicle_analysis": vehicle_analysis,
        "violation_analysis": violation_analysis,
        "accident_analysis": accident_analysis
    }

# =====================================================
# COMPUTER VISION
# =====================================================

@app.get("/cv/status")
def cv_status():
    return get_cv_status()


@app.post("/cv/simulate")
def cv_simulate(
    db: Session = Depends(get_db)
):
    return simulate_detection(db)

@app.get("/cv/detections")
def cv_detections(
    db: Session = Depends(get_db)
):
    return get_detections(db)


@app.get("/cv/analytics")
def cv_analytics(
    db: Session = Depends(get_db)
):
    return get_cv_analytics(db)

# =====================================================
# VEHICLE TRACKING
# =====================================================

@app.get("/tracking")
def tracking_data(
    db: Session = Depends(get_db)
):
    return get_tracking_data(db)


@app.get("/tracking/analytics")
def tracking_analytics(
    db: Session = Depends(get_db)
):
    records = get_tracking_data(db)

    total = len(records)

    cars = len([
        x for x in records
        if x["vehicle_type"] == "car"
    ])

    trucks = len([
        x for x in records
        if x["vehicle_type"] == "truck"
    ])

    buses = len([
        x for x in records
        if x["vehicle_type"] == "bus"
    ])

    motorcycles = len([
        x for x in records
        if x["vehicle_type"] == "motorcycle"
    ])

    return {
        "total_tracked": total,
        "cars": cars,
        "trucks": trucks,
        "buses": buses,
        "motorcycles": motorcycles
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
# TRAFFIC FLOW ANALYTICS
# =====================================================

@app.post("/traffic-flow/generate")
def traffic_flow_generate(
    db: Session = Depends(get_db)
):

    flow = generate_traffic_flow(db)

    return {
        "message": "Traffic flow generated",
        "traffic_status": flow.traffic_status,
        "total_vehicles": flow.total_vehicles
    }


@app.get("/traffic-flow")
def get_traffic_flow(
    db: Session = Depends(get_db)
):

    records = db.query(
        TrafficFlow
    ).all()

    result = []

    for row in records:

        result.append({
            "id": row.id,
            "total_vehicles": row.total_vehicles,
            "cars": row.cars,
            "trucks": row.trucks,
            "buses": row.buses,
            "motorcycles": row.motorcycles,
            "traffic_status": row.traffic_status,
            "timestamp": str(row.timestamp)
        })

    return result

# =====================================================
# VIOLATIONS
# =====================================================

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


# =====================================================
# ALERTS
# =====================================================

@app.post("/alerts/test")
def create_test_alert(
    db: Session = Depends(get_db)
):
    alert = create_alert(
        db,
        "TEST_ALERT",
        "MEDIUM",
        "This is a test alert"
    )

    return {
        "id": alert.id,
        "message": "Test alert created"
    }


@app.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db)
):
    alerts = get_all_alerts(db)

    return [
        {
            "id": alert.id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "status": alert.status,
            "created_at": str(alert.created_at)
        }
        for alert in alerts
    ]


@app.get("/alerts/{alert_id}")
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = get_alert_by_id(
        db,
        alert_id
    )

    if not alert:
        return {
            "error": "Alert not found"
        }

    return {
        "id": alert.id,
        "alert_type": alert.alert_type,
        "severity": alert.severity,
        "message": alert.message,
        "status": alert.status,
        "created_at": str(alert.created_at)
    }


@app.delete("/alerts/{alert_id}")
def remove_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_alert(
        db,
        alert_id
    )

    if not deleted:
        return {
            "error": "Alert not found"
        }

    return {
        "message": "Alert deleted"
    }


# =====================================================
# ML RISK PREDICTION
# =====================================================

@app.post("/predict-risk")
def predict_risk(
    hour: int,
    day_of_week: int,
    traffic_density: int,
    rainfall: int,
    visibility: int,
    speed_avg: int,
    junction_score: int,
    db: Session = Depends(get_db)
):
    prediction = predict_accident_risk(
        hour,
        day_of_week,
        traffic_density,
        rainfall,
        visibility,
        speed_avg,
        junction_score
    )

    risk_level = "HIGH" if prediction == 1 else "LOW"

    if prediction == 1:
        create_alert(
            db,
            "ACCIDENT_RISK",
            "HIGH",
            "High accident risk detected"
        )

    return {
        "prediction": prediction,
        "risk_level": risk_level,
        "hour": hour,
        "day_of_week": day_of_week,
        "traffic_density": traffic_density,
        "rainfall": rainfall,
        "visibility": visibility,
        "speed_avg": speed_avg,
        "junction_score": junction_score
    }

@app.post("/near-miss/generate")
def generate_near_miss(
    db: Session = Depends(get_db)
):

    event = generate_near_miss_event(db)

    return {
        "message": "Near miss detected",
        "vehicle_a": event.vehicle_a,
        "vehicle_b": event.vehicle_b,
        "distance": event.distance,
        "risk_level": event.risk_level
    }


@app.get("/near-miss")
def get_near_miss(
    db: Session = Depends(get_db)
):

    events = get_near_miss_events(db)

    result = []

    for event in events:

        result.append({
            "id": event.id,
            "vehicle_a": event.vehicle_a,
            "vehicle_b": event.vehicle_b,
            "distance": event.distance,
            "risk_level": event.risk_level,
            "timestamp": str(event.timestamp)
        })

    return result


@app.get("/near-miss/analytics")
def near_miss_analytics(
    db: Session = Depends(get_db)
):

    return get_near_miss_analytics(db)