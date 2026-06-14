from models import (
    AccidentRisk,
    EmergencyResponse
)


def generate_emergency_response(db):

    latest_risk = (
        db.query(AccidentRisk)
        .order_by(
            AccidentRisk.id.desc()
        )
        .first()
    )

    if not latest_risk:
        return None

    if latest_risk.risk_score >= 80:

        level = "CRITICAL"
        action = "Dispatch Ambulance"
        time = 5

    elif latest_risk.risk_score >= 50:

        level = "WARNING"
        action = "Alert Traffic Police"
        time = 10

    else:

        level = "NORMAL"
        action = "Monitor Situation"
        time = 20

    response = EmergencyResponse(
        emergency_level=level,
        response_action=action,
        estimated_time=time,
        risk_score=latest_risk.risk_score
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    return response


def get_emergency_analytics(db):

    responses = db.query(
        EmergencyResponse
    ).all()

    critical = len([
        r for r in responses
        if r.emergency_level == "CRITICAL"
    ])

    warning = len([
        r for r in responses
        if r.emergency_level == "WARNING"
    ])

    normal = len([
        r for r in responses
        if r.emergency_level == "NORMAL"
    ])

    return {
        "total_responses": len(responses),
        "critical": critical,
        "warning": warning,
        "normal": normal
    }