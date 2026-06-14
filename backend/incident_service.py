from models import (
    EmergencyResponse,
    AccidentRisk,
    Incident
)


def generate_incident(db):

    latest_emergency = (
        db.query(EmergencyResponse)
        .order_by(
            EmergencyResponse.id.desc()
        )
        .first()
    )

    latest_risk = (
        db.query(AccidentRisk)
        .order_by(
            AccidentRisk.id.desc()
        )
        .first()
    )

    if not latest_emergency:
        return None

    count = (
        db.query(Incident)
        .count()
    ) + 1

    incident_id = (
        f"INC_{count}"
    )

    if latest_emergency.emergency_level == "CRITICAL":

        priority = "HIGH"
        team = "Emergency Team"

    elif latest_emergency.emergency_level == "WARNING":

        priority = "MEDIUM"
        team = "Traffic Team"

    else:

        priority = "LOW"
        team = "Monitoring Team"

    incident = Incident(
        incident_id=incident_id,
        risk_level=latest_risk.risk_level,
        emergency_level=latest_emergency.emergency_level,
        priority=priority,
        assigned_team=team,
        status="OPEN"
    )

    db.add(incident)

    db.commit()

    db.refresh(incident)

    return incident


def get_incidents(db):

    return (
        db.query(Incident)
        .all()
    )


def get_incident_analytics(db):

    incidents = (
        db.query(Incident)
        .all()
    )

    high = len([
        i for i in incidents
        if i.priority == "HIGH"
    ])

    medium = len([
        i for i in incidents
        if i.priority == "MEDIUM"
    ])

    low = len([
        i for i in incidents
        if i.priority == "LOW"
    ])

    return {
        "total_incidents": len(incidents),
        "high_priority": high,
        "medium_priority": medium,
        "low_priority": low
    }