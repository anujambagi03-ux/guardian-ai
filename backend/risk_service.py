from models import (
    TrafficFlow,
    NearMissEvent,
    AccidentRisk
)


def generate_risk_score(db):

    latest_flow = (
        db.query(TrafficFlow)
        .order_by(TrafficFlow.id.desc())
        .first()
    )

    near_miss_count = (
        db.query(NearMissEvent)
        .count()
    )

    if not latest_flow:

        return None

    score = 0

    if latest_flow.traffic_status == "LOW":
        score += 20

    elif latest_flow.traffic_status == "MEDIUM":
        score += 50

    elif latest_flow.traffic_status == "HEAVY":
        score += 80

    score += near_miss_count * 5

    if score > 100:
        score = 100

    if score >= 80:
        risk_level = "HIGH"
        recommendation = "Deploy traffic patrol"

    elif score >= 50:
        risk_level = "MEDIUM"
        recommendation = "Monitor traffic closely"

    else:
        risk_level = "LOW"
        recommendation = "Normal traffic"

    risk = AccidentRisk(
        risk_score=score,
        risk_level=risk_level,
        traffic_status=latest_flow.traffic_status,
        near_miss_count=near_miss_count,
        recommendation=recommendation
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)

    return risk


def get_risk_analytics(db):

    risks = db.query(
        AccidentRisk
    ).all()

    high = len([
        r for r in risks
        if r.risk_level == "HIGH"
    ])

    medium = len([
        r for r in risks
        if r.risk_level == "MEDIUM"
    ])

    low = len([
        r for r in risks
        if r.risk_level == "LOW"
    ])

    return {
        "total_predictions": len(risks),
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low
    }