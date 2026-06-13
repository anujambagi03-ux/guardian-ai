from sqlalchemy.orm import Session

from models import DetectionFrame


def get_cv_status():
    return {
        "module": "Computer Vision",
        "status": "ACTIVE",
        "model": "YOLOv8"
    }


def save_real_detection(
    db: Session,
    vehicle_counts
):
    total = sum(
        vehicle_counts.values()
    )

    frame = DetectionFrame(
        frame_id=f"FRAME_{db.query(DetectionFrame).count()+1}",
        vehicle_count=total,
        cars=vehicle_counts.get(
            "car",
            0
        ),
        trucks=vehicle_counts.get(
            "truck",
            0
        ),
        buses=vehicle_counts.get(
            "bus",
            0
        ),
        motorcycles=vehicle_counts.get(
            "motorcycle",
            0
        )
    )

    db.add(frame)
    db.commit()
    db.refresh(frame)

    return frame


def simulate_detection(
    db: Session
):
    frame = DetectionFrame(
        frame_id=f"FRAME_{db.query(DetectionFrame).count()+1}",
        vehicle_count=5,
        cars=3,
        trucks=1,
        buses=1,
        motorcycles=0
    )

    db.add(frame)
    db.commit()

    return {
        "message": "Detection simulated"
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
            "cars": frame.cars,
            "trucks": frame.trucks,
            "buses": frame.buses,
            "motorcycles": frame.motorcycles,
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

    total_frames = len(
        frames
    )

    total_vehicles = sum(
        x.vehicle_count
        for x in frames
    )

    total_cars = sum(
        x.cars
        for x in frames
    )

    total_trucks = sum(
        x.trucks
        for x in frames
    )

    total_buses = sum(
        x.buses
        for x in frames
    )

    total_motorcycles = sum(
        x.motorcycles
        for x in frames
    )

    average = 0

    if total_frames > 0:
        average = round(
            total_vehicles /
            total_frames,
            2
        )

    return {
        "total_frames": total_frames,
        "total_vehicles": total_vehicles,
        "average_vehicles": average,
        "cars": total_cars,
        "trucks": total_trucks,
        "buses": total_buses,
        "motorcycles": total_motorcycles
    }