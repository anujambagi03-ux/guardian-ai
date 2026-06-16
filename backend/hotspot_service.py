from sqlalchemy.orm import Session

from models import (
    Incident,
    AccidentRisk,
    IncidentPattern,
    Hotspot
)


def generate_hotspot(db: Session):

    incident_count = (
        db.query(
            Incident
        ).count()
    )

    latest_risk = (
        db.query(
            AccidentRisk
        )
        .order_by(
            AccidentRisk.id.desc()
        )
        .first()
    )

    latest_pattern = (
        db.query(
            IncidentPattern
        )
        .order_by(
            IncidentPattern.id.desc()
        )
        .first()
    )

    if not latest_risk:

        return {
            "error":
            "No risk data available"
        }

    hotspot_score = (
        incident_count +
        latest_risk.risk_score
    )

    if hotspot_score >= 90:

        severity = "CRITICAL"
        rank = 1

    elif hotspot_score >= 70:

        severity = "HIGH"
        rank = 2

    elif hotspot_score >= 40:

        severity = "MEDIUM"
        rank = 3

    else:

        severity = "LOW"
        rank = 4

    count = (
        db.query(
            Hotspot
        ).count()
    ) + 1

    hotspot = Hotspot(
        hotspot_id=
        f"HOTSPOT_{count}",

        location=
        "CITY_CENTER",

        hotspot_type=
        (
            latest_pattern.pattern_type
            if latest_pattern
            else "INCIDENT_CLUSTER"
        ),

        incident_count=
        incident_count,

        risk_score=
        hotspot_score,

        severity_level=
        severity,

        rank=
        rank
    )

    db.add(
        hotspot
    )

    db.commit()

    db.refresh(
        hotspot
    )

    return {
        "message":
        "Hotspot generated",

        "hotspot_id":
        hotspot.hotspot_id,

        "severity_level":
        hotspot.severity_level,

        "rank":
        hotspot.rank
    }


def get_hotspots(db: Session):

    return (
        db.query(
            Hotspot
        ).all()
    )


def get_hotspot_analytics(db: Session):

    hotspots = (
        db.query(
            Hotspot
        ).all()
    )

    critical = len([
        h for h in hotspots
        if h.severity_level
        == "CRITICAL"
    ])

    high = len([
        h for h in hotspots
        if h.severity_level
        == "HIGH"
    ])

    medium = len([
        h for h in hotspots
        if h.severity_level
        == "MEDIUM"
    ])

    low = len([
        h for h in hotspots
        if h.severity_level
        == "LOW"
    ])

    return {

        "total_hotspots":
        len(hotspots),

        "critical_hotspots":
        critical,

        "high_hotspots":
        high,

        "medium_hotspots":
        medium,

        "low_hotspots":
        low
    }