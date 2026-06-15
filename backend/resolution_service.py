from models import (
    ResponseTracking,
    ResolutionCase
)


def create_resolution(db):

    latest_response = (
        db.query(ResponseTracking)
        .order_by(
            ResponseTracking.id.desc()
        )
        .first()
    )

    if not latest_response:
        return None

    count = (
        db.query(ResolutionCase)
        .count()
    ) + 1

    resolution_id = (
        f"RES_{count}"
    )

    if latest_response.response_status == "EN_ROUTE":

        resolution_status = "RESOLVED"

        resolution_notes = (
            "Emergency handled successfully"
        )

        closure_time = 25

    else:

        resolution_status = "PENDING"

        resolution_notes = (
            "Awaiting completion"
        )

        closure_time = 0

    resolution = ResolutionCase(
        resolution_id=resolution_id,
        response_id=latest_response.response_id,
        incident_id=latest_response.incident_id,
        resolution_status=resolution_status,
        resolution_notes=resolution_notes,
        closure_time_minutes=closure_time
    )

    db.add(resolution)

    db.commit()

    db.refresh(resolution)

    return resolution


def get_resolutions(db):

    return (
        db.query(
            ResolutionCase
        )
        .all()
    )


def get_resolution_analytics(db):

    resolutions = (
        db.query(
            ResolutionCase
        )
        .all()
    )

    resolved = len([
        r for r in resolutions
        if r.resolution_status == "RESOLVED"
    ])

    pending = len([
        r for r in resolutions
        if r.resolution_status == "PENDING"
    ])

    avg_time = 0

    if len(resolutions) > 0:

        avg_time = (
            sum(
                r.closure_time_minutes
                for r in resolutions
            )
            / len(resolutions)
        )

    return {
        "total_cases": len(resolutions),
        "resolved_cases": resolved,
        "pending_cases": pending,
        "average_closure_time": avg_time
    }