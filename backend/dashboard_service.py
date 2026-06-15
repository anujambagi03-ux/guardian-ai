from models import (
    TrafficFlow,
    AccidentRisk,
    Incident,
    Dispatch,
    ResponseTracking,
    ResolutionCase,
    ResourceUnit
)


def get_dashboard_overview(db):

    latest_traffic = (
        db.query(TrafficFlow)
        .order_by(TrafficFlow.id.desc())
        .first()
    )

    latest_risk = (
        db.query(AccidentRisk)
        .order_by(AccidentRisk.id.desc())
        .first()
    )

    active_incidents = (
        db.query(Incident)
        .count()
    )

    active_dispatches = (
        db.query(Dispatch)
        .count()
    )

    active_responses = (
        db.query(ResponseTracking)
        .count()
    )

    resolved_cases = (
        db.query(ResolutionCase)
        .count()
    )

    available_resources = len([
        r for r in db.query(
            ResourceUnit
        ).all()
        if r.availability_status == "AVAILABLE"
    ])

    return {
        "traffic_status":
            latest_traffic.traffic_status
            if latest_traffic else "UNKNOWN",

        "risk_level":
            latest_risk.risk_level
            if latest_risk else "UNKNOWN",

        "active_incidents":
            active_incidents,

        "active_dispatches":
            active_dispatches,

        "active_responses":
            active_responses,

        "resolved_cases":
            resolved_cases,

        "available_resources":
            available_resources
    }


def get_system_summary(db):

    return {
        "vehicles_detected":
            db.query(TrafficFlow).count(),

        "risk_records":
            db.query(AccidentRisk).count(),

        "incidents":
            db.query(Incident).count(),

        "dispatches":
            db.query(Dispatch).count(),

        "responses":
            db.query(ResponseTracking).count(),

        "resolutions":
            db.query(ResolutionCase).count(),

        "resources":
            db.query(ResourceUnit).count()
    }