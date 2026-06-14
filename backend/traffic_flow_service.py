from models import (
    TrafficFlow,
    TrackedVehicle
)


def generate_traffic_flow(db):

    vehicles = db.query(
        TrackedVehicle
    ).all()

    total = len(vehicles)

    cars = len([
        x for x in vehicles
        if x.vehicle_type == "car"
    ])

    trucks = len([
        x for x in vehicles
        if x.vehicle_type == "truck"
    ])

    buses = len([
        x for x in vehicles
        if x.vehicle_type == "bus"
    ])

    motorcycles = len([
        x for x in vehicles
        if x.vehicle_type == "motorcycle"
    ])

    if total < 100:
        status = "LOW"

    elif total < 500:
        status = "MEDIUM"

    else:
        status = "HEAVY"

    flow = TrafficFlow(
        total_vehicles=total,
        cars=cars,
        trucks=trucks,
        buses=buses,
        motorcycles=motorcycles,
        traffic_status=status
    )

    db.add(flow)
    db.commit()

    return flow