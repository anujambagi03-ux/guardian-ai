from database import SessionLocal
from models import Accident


def save_detected_accidents(accidents):

    db = SessionLocal()

    try:

        for accident in accidents:

            accident_record = Accident(
                location=accident["location"],
                severity=accident["severity"]
            )

            db.add(accident_record)

        db.commit()

    finally:
        db.close()