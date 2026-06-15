from models import (
    TrafficFlow,
    AccidentRisk,
    AIRecommendation
)


def generate_recommendation(db):

    latest_traffic = (
        db.query(TrafficFlow)
        .order_by(
            TrafficFlow.id.desc()
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

    if not latest_traffic or not latest_risk:
        return None

    recommendation_text = (
        "Continue monitoring"
    )

    priority = "LOW"

    if (
        latest_traffic.traffic_status
        == "HEAVY"
    ):
        recommendation_text = (
            "Deploy traffic police and activate alternate routes"
        )

        priority = "HIGH"

    if (
        latest_risk.risk_level
        == "HIGH"
    ):
        recommendation_text += (
            " | Deploy ambulance and emergency team"
        )

        priority = "CRITICAL"

    count = (
        db.query(
            AIRecommendation
        )
        .count()
    ) + 1

    recommendation_id = (
        f"REC_{count}"
    )

    recommendation = AIRecommendation(
        recommendation_id=
        recommendation_id,

        traffic_status=
        latest_traffic.traffic_status,

        risk_level=
        latest_risk.risk_level,

        recommendation=
        recommendation_text,

        priority=
        priority
    )

    db.add(
        recommendation
    )

    db.commit()

    db.refresh(
        recommendation
    )

    return recommendation


def get_recommendations(db):

    return (
        db.query(
            AIRecommendation
        )
        .all()
    )


def get_recommendation_analytics(db):

    recommendations = (
        db.query(
            AIRecommendation
        )
        .all()
    )

    critical = len([
        r for r in recommendations
        if r.priority
        == "CRITICAL"
    ])

    high = len([
        r for r in recommendations
        if r.priority
        == "HIGH"
    ])

    low = len([
        r for r in recommendations
        if r.priority
        == "LOW"
    ])

    return {
        "total_recommendations":
            len(recommendations),

        "critical_priority":
            critical,

        "high_priority":
            high,

        "low_priority":
            low
    }