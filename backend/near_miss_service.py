from sqlalchemy.orm import Session

from models import NearMissEvent


def generate_near_miss_event(db: Session):

    event = NearMissEvent(
        vehicle_a="TRACK_1",
        vehicle_b="TRACK_2",
        distance=15,
        risk_level="HIGH"
    )

    db.add(event)

    db.commit()

    return event


def get_near_miss_events(db: Session):

    return db.query(
        NearMissEvent
    ).all()


def get_near_miss_analytics(db: Session):

    events = db.query(
        NearMissEvent
    ).all()

    high = 0
    medium = 0
    low = 0

    for event in events:

        if event.risk_level == "HIGH":
            high += 1

        elif event.risk_level == "MEDIUM":
            medium += 1

        else:
            low += 1

    return {
        "total_events": len(events),
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low
    }