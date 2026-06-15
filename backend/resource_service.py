from models import (
    ResolutionCase,
    ResourceUnit
)


def generate_resource_allocation(db):

    latest_case = (
        db.query(ResolutionCase)
        .order_by(
            ResolutionCase.id.desc()
        )
        .first()
    )

    if not latest_case:
        return None

    count = (
        db.query(ResourceUnit)
        .count()
    ) + 1

    resource_id = f"RSRC_{count}"

    resource = ResourceUnit(
        resource_id=resource_id,
        resource_type="Ambulance",
        availability_status="AVAILABLE",
        current_location="City Control Center",
        utilization_score=85
    )

    db.add(resource)

    db.commit()

    db.refresh(resource)

    return resource


def get_resources(db):

    return (
        db.query(
            ResourceUnit
        )
        .all()
    )


def get_resource_analytics(db):

    resources = (
        db.query(
            ResourceUnit
        )
        .all()
    )

    available = len([
        r for r in resources
        if r.availability_status
        == "AVAILABLE"
    ])

    unavailable = len([
        r for r in resources
        if r.availability_status
        == "BUSY"
    ])

    avg_utilization = 0

    if len(resources) > 0:

        avg_utilization = (
            sum(
                r.utilization_score
                for r in resources
            )
            / len(resources)
        )

    return {
        "total_resources":
            len(resources),
        "available_resources":
            available,
        "busy_resources":
            unavailable,
        "average_utilization":
            avg_utilization
    }