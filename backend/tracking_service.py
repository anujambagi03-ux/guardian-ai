from sqlalchemy.orm import Session

from models import TrackedVehicle


def create_tracking_records(
    db: Session,
    vehicle_counts
):
    created = []

    counter = db.query(
        TrackedVehicle
    ).count()

    for vehicle_type, count in vehicle_counts.items():

        for i in range(count):

            counter += 1

            tracking_id = (
                f"TRACK_{counter}"
            )

            vehicle = TrackedVehicle(
                tracking_id=tracking_id,
                vehicle_type=vehicle_type,
                confidence="YOLO"
            )

            db.add(vehicle)

            created.append(
                tracking_id
            )

    db.commit()

    return created


def get_tracking_data(
    db: Session
):
    vehicles = db.query(
        TrackedVehicle
    ).all()

    result = []

    for vehicle in vehicles:

        result.append({
            "id": vehicle.id,
            "tracking_id": vehicle.tracking_id,
            "vehicle_type": vehicle.vehicle_type,
            "confidence": vehicle.confidence,
            "created_at": str(
                vehicle.created_at
            )
        })

    return result