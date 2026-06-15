from models import (
    TrafficFlow,
    TrafficTrend
)


def generate_traffic_trend(db):

    traffic_records = (
        db.query(TrafficFlow)
        .all()
    )

    if len(traffic_records) == 0:
        return None

    count = (
        db.query(
            TrafficTrend
        ).count()
    ) + 1

    trend_id = f"TREND_{count}"

    avg_vehicles = int(
        sum(
            t.total_vehicles
            for t in traffic_records
        )
        / len(traffic_records)
    )

    latest_status = (
        traffic_records[-1]
        .traffic_status
    )

    if avg_vehicles > 1000:

        direction = "INCREASING"

    elif avg_vehicles > 500:

        direction = "STABLE"

    else:

        direction = "DECREASING"

    trend = TrafficTrend(
        trend_id=trend_id,
        average_vehicle_count=avg_vehicles,
        traffic_status=latest_status,
        trend_direction=direction
    )

    db.add(trend)

    db.commit()

    db.refresh(trend)

    return trend


def get_traffic_trends(db):

    return (
        db.query(
            TrafficTrend
        )
        .all()
    )


def get_traffic_summary(db):

    trends = (
        db.query(
            TrafficTrend
        )
        .all()
    )

    increasing = len([
        t for t in trends
        if t.trend_direction
        == "INCREASING"
    ])

    stable = len([
        t for t in trends
        if t.trend_direction
        == "STABLE"
    ])

    decreasing = len([
        t for t in trends
        if t.trend_direction
        == "DECREASING"
    ])

    return {
        "total_trends":
            len(trends),

        "increasing_trends":
            increasing,

        "stable_trends":
            stable,

        "decreasing_trends":
            decreasing
    }