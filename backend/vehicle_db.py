from database import SessionLocal
from models import Vehicle
import uuid


def save_detected_vehicles(vehicle_counts):

    db = SessionLocal()

    try:

        for vehicle_type, count in vehicle_counts.items():

            for i in range(count):

                unique_id = str(uuid.uuid4())[:8]

                vehicle = Vehicle(
                    vehicle_number=f"{vehicle_type.upper()}-{unique_id}",
                    vehicle_type=vehicle_type
                )

                db.add(vehicle)

        db.commit()

    finally:
        db.close()