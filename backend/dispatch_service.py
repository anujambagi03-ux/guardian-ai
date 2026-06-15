from models import (
    Incident,
    Dispatch
)


def generate_dispatch(db):

    latest_incident = (
        db.query(Incident)
        .order_by(
            Incident.id.desc()
        )
        .first()
    )

    if not latest_incident:
        return None

    count = (
        db.query(Dispatch)
        .count()
    ) + 1

    dispatch_id = (
        f"DSP_{count}"
    )

    if latest_incident.priority == "HIGH":

        vehicle = "Ambulance"
        personnel = 4

    elif latest_incident.priority == "MEDIUM":

        vehicle = "Police Vehicle"
        personnel = 2

    else:

        vehicle = "Monitoring Vehicle"
        personnel = 1

    dispatch = Dispatch(
        dispatch_id=dispatch_id,
        incident_id=latest_incident.incident_id,
        vehicle_type=vehicle,
        personnel_count=personnel,
        dispatch_status="DISPATCHED"
    )

    db.add(dispatch)

    db.commit()

    db.refresh(dispatch)

    return dispatch


def get_dispatches(db):

    return (
        db.query(Dispatch)
        .all()
    )


def get_dispatch_analytics(db):

    dispatches = (
        db.query(Dispatch)
        .all()
    )

    dispatched = len([
        d for d in dispatches
        if d.dispatch_status == "DISPATCHED"
    ])

    return {
        "total_dispatches": len(dispatches),
        "active_dispatches": dispatched
    }