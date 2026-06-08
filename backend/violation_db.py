from database import SessionLocal
from models import Violation


def save_detected_violations(violations):

    db = SessionLocal()

    try:

        for violation in violations:

            violation_record = Violation(
                vehicle_number=violation["vehicle_number"],
                violation_type=violation["violation_type"],
                location=violation["location"]
            )

            db.add(violation_record)

        db.commit()

    finally:
        db.close()