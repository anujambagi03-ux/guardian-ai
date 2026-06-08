from database import SessionLocal
from models import Vehicle


def save_detected_vehicles(vehicle_counts):

    db = SessionLocal()

    try:

        for vehicle_type, count in vehicle_counts.items():

            for i in range(count):

                vehicle = Vehicle(
                    vehicle_number=f"AUTO-{vehicle_type[:3].upper()}-{i}",
                    vehicle_type=vehicle_type
                )

                db.add(vehicle)

        db.commit()

    finally:
        db.close()