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