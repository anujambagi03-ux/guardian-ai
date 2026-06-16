from datetime import datetime

from models import (
    PredictiveIncidentIntelligence,
    TemporalTrafficIntelligence
)


def generate_predictive_incidents(db):

    db.query(PredictiveIncidentIntelligence).delete()

    temporal_records = db.query(
        TemporalTrafficIntelligence
    ).all()

    count = 0

    for record in temporal_records:

        predicted_incidents = max(
            1,
            int(record.risk_score / 10)
        )

        confidence = min(
            95,
            60 + int(record.risk_score / 2)
        )

        severity = "LOW"

        if record.risk_score >= 70:
            severity = "HIGH"
        elif record.risk_score >= 40:
            severity = "MEDIUM"

        recommendation = (
            "Increase patrol monitoring"
            if severity != "LOW"
            else "Routine monitoring"
        )

        prediction = PredictiveIncidentIntelligence(
            prediction_id=f"PRED_{record.hour_of_day}",
            zone_id="CITY_ZONE",
            predicted_hour=record.hour_of_day,
            predicted_incidents=predicted_incidents,
            risk_score=int(record.risk_score),
            severity_level=severity,
            confidence_score=confidence,
            recommendation=recommendation,
            created_at=datetime.utcnow()
        )
        db.add(prediction)

        count += 1

    db.commit()

    return count