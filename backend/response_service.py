from models import (
    Dispatch,
    ResponseTracking
)


def generate_response_tracking(db):

    latest_dispatch = (
        db.query(Dispatch)
        .order_by(
            Dispatch.id.desc()
        )
        .first()
    )

    if not latest_dispatch:
        return None

    count = (
        db.query(ResponseTracking)
        .count()
    ) + 1

    response_id = (
        f"RSP_{count}"
    )

    status = "EN_ROUTE"

    response = ResponseTracking(
        response_id=response_id,
        dispatch_id=latest_dispatch.dispatch_id,
        incident_id=latest_dispatch.incident_id,
        response_status=status
    )

    db.add(response)

    db.commit()

    db.refresh(response)

    return response


def get_response_tracking(db):

    return (
        db.query(ResponseTracking)
        .all()
    )


def get_response_analytics(db):

    responses = (
        db.query(ResponseTracking)
        .all()
    )

    active = len([
        r for r in responses
        if r.response_status != "CLOSED"
    ])

    closed = len([
        r for r in responses
        if r.response_status == "CLOSED"
    ])

    return {
        "total_responses": len(responses),
        "active_cases": active,
        "closed_cases": closed
    }