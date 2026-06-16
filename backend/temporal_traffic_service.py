from database import SessionLocal

from models import (
    Incident,
    TemporalTrafficIntelligence
)

from collections import defaultdict


def generate_temporal_intelligence():

    db = SessionLocal()

    try:

        db.query(TemporalTrafficIntelligence).delete()

        incidents = db.query(Incident).all()

        hourly_stats = defaultdict(int)

        for incident in incidents:

            if incident.created_at:

                hour = incident.created_at.hour

                hourly_stats[hour] += 1

        records_created = 0

        for hour in range(24):

            count = hourly_stats.get(hour, 0)

            risk_score = min(count * 10, 100)

            if risk_score >= 80:
                risk_level = "HIGH"
            elif risk_score >= 50:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

            if 6 <= hour < 12:
                peak_period = "MORNING"
            elif 12 <= hour < 18:
                peak_period = "AFTERNOON"
            elif 18 <= hour < 24:
                peak_period = "EVENING"
            else:
                peak_period = "NIGHT"

            record = TemporalTrafficIntelligence(
                hour_of_day=hour,
                incident_count=count,
                risk_score=risk_score,
                risk_level=risk_level,
                peak_period=peak_period
            )

            db.add(record)

            records_created += 1

        db.commit()

        return {
            "message": "Temporal intelligence generated",
            "records": records_created
        }

    finally:
        db.close()