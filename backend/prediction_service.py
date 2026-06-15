from models import (
    TrafficFlow,
    TrafficPrediction
)


def generate_prediction(db):

    latest_flow = (
        db.query(TrafficFlow)
        .order_by(
            TrafficFlow.id.desc()
        )
        .first()
    )

    if not latest_flow:
        return None

    count = (
        db.query(
            TrafficPrediction
        ).count()
    ) + 1

    prediction_id = f"PRED_{count}"

    current_status = (
        latest_flow.traffic_status
    )

    if current_status == "HEAVY":

        predicted = "SEVERE"

        confidence = 92

    elif current_status == "MODERATE":

        predicted = "HEAVY"

        confidence = 85

    else:

        predicted = "MODERATE"

        confidence = 78

    prediction = TrafficPrediction(
        prediction_id=prediction_id,
        current_traffic=current_status,
        predicted_traffic=predicted,
        confidence_score=confidence,
        prediction_window="30 Minutes"
    )

    db.add(prediction)

    db.commit()

    db.refresh(prediction)

    return prediction


def get_predictions(db):

    return (
        db.query(
            TrafficPrediction
        )
        .all()
    )


def get_prediction_analytics(db):

    predictions = (
        db.query(
            TrafficPrediction
        )
        .all()
    )

    if len(predictions) == 0:

        return {
            "total_predictions": 0,
            "average_confidence": 0
        }

    avg_confidence = (
        sum(
            p.confidence_score
            for p in predictions
        )
        / len(predictions)
    )

    return {
        "total_predictions":
            len(predictions),
        "average_confidence":
            avg_confidence
    }