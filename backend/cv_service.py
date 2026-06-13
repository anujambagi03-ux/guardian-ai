from sqlalchemy.orm import Session

from models import DetectionFrame


def get_cv_status():
    return {
        "module": "Computer Vision",
        "status": "ACTIVE",
        "model": "Simulation Mode"
    }


def simulate_detection(
    db: Session
):
    frame = DetectionFrame(
        frame_id="FRAME_" + str(
            db.query(
                DetectionFrame
            ).count() + 1
        ),
        vehicle_count=5
    )

    db.add(frame)
    db.commit()
    db.refresh(frame)

    return {
        "message": "Detection simulated",
        "frame_id": frame.frame_id,
        "vehicle_count": frame.vehicle_count
    }


def get_detections(
    db: Session
):
    frames = db.query(
        DetectionFrame
    ).order_by(
        DetectionFrame.id.desc()
    ).all()

    result = []

    for frame in frames:
        result.append({
            "id": frame.id,
            "frame_id": frame.frame_id,
            "vehicle_count": frame.vehicle_count,
            "timestamp": str(
                frame.timestamp
            )
        })

    return result


def get_cv_analytics(
    db: Session
):
    frames = db.query(
        DetectionFrame
    ).all()

    total_frames = len(frames)

    total_vehicles = sum(
        frame.vehicle_count
        for frame in frames
    )

    avg_vehicles = 0

    if total_frames > 0:
        avg_vehicles = round(
            total_vehicles / total_frames,
            2
        )

    risk_level = "LOW"

    if avg_vehicles >= 10:
        risk_level = "HIGH"

    elif avg_vehicles >= 5:
        risk_level = "MEDIUM"

    return {
        "total_frames": total_frames,
        "total_vehicles": total_vehicles,
        "average_vehicles": avg_vehicles,
        "risk_level": risk_level
    }