from sqlalchemy.orm import Session

from models import (
    Incident,
    AccidentRisk,
    AIRecommendation,
    AIDecision,
    IncidentPattern
)


def generate_incident_pattern(db: Session):

    incidents = db.query(
        Incident
    ).all()

    latest_risk = (
        db.query(AccidentRisk)
        .order_by(
            AccidentRisk.id.desc()
        )
        .first()
    )

    recommendation_count = (
        db.query(
            AIRecommendation
        ).count()
    )

    decision_count = (
        db.query(
            AIDecision
        ).count()
    )

    incident_count = len(
        incidents
    )

    if not latest_risk:
        return {
            "error":
            "No risk data available"
        }

    pattern_type = (
        "INCIDENT_CLUSTER"
    )

    if incident_count >= 10:

        trend = "ESCALATING"

    elif incident_count >= 5:

        trend = "STABLE"

    else:

        trend = "NORMAL"

    count = (
        db.query(
            IncidentPattern
        ).count()
    ) + 1

    pattern = IncidentPattern(
        pattern_id=
        f"PATTERN_{count}",

        pattern_type=
        pattern_type,

        risk_level=
        latest_risk.risk_level,

        incident_count=
        incident_count,

        recommendation_count=
        recommendation_count,

        decision_count=
        decision_count,

        trend=
        trend
    )

    db.add(pattern)

    db.commit()

    db.refresh(pattern)

    return {
        "message":
        "Incident pattern generated",

        "pattern_id":
        pattern.pattern_id,

        "pattern_type":
        pattern.pattern_type,

        "risk_level":
        pattern.risk_level,

        "trend":
        pattern.trend
    }


def get_incident_patterns(db: Session):

    return (
        db.query(
            IncidentPattern
        ).all()
    )


def get_pattern_analytics(db: Session):

    patterns = (
        db.query(
            IncidentPattern
        ).all()
    )

    high_risk = len([
        p for p in patterns
        if p.risk_level == "HIGH"
    ])

    escalating = len([
        p for p in patterns
        if p.trend == "ESCALATING"
    ])

    stable = len([
        p for p in patterns
        if p.trend == "STABLE"
    ])

    return {

        "total_patterns":
        len(patterns),

        "high_risk_patterns":
        high_risk,

        "escalating_patterns":
        escalating,

        "stable_patterns":
        stable
    }