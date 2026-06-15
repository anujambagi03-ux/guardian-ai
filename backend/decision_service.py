from sqlalchemy.orm import Session

from models import (
    AIRecommendation,
    AIDecision
)


def generate_decision(db: Session):

    recommendation = (
        db.query(AIRecommendation)
        .order_by(
            AIRecommendation.id.desc()
        )
        .first()
    )

    if not recommendation:
        return {
            "error": "No recommendation data available"
        }

    decision_type = "TRAFFIC_MANAGEMENT"

    if recommendation.priority == "CRITICAL":
        decision_type = "EMERGENCY_RESPONSE"

    decision = AIDecision(
        decision_id=f"DEC_{recommendation.id}",
        decision_type=decision_type,
        priority=recommendation.priority,
        action_plan=recommendation.recommendation,
        execution_status="PENDING"
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return {
        "message": "AI decision generated",
        "decision_id": decision.decision_id,
        "decision_type": decision.decision_type,
        "priority": decision.priority,
        "execution_status": decision.execution_status
    }


def get_decisions(db: Session):

    decisions = db.query(
        AIDecision
    ).all()

    return decisions


def get_decision_analytics(db: Session):

    decisions = db.query(
        AIDecision
    ).all()

    total = len(decisions)

    pending = len(
        [
            d for d in decisions
            if d.execution_status == "PENDING"
        ]
    )

    return {
        "total_decisions": total,
        "pending_decisions": pending
    }