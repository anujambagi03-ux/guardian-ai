from sqlalchemy.orm import Session

from models import Vehicle
from models import Violation
from models import Accident


def generate_analytics(db: Session):

    total_vehicles = db.query(
        Vehicle
    ).count()

    cars = db.query(
        Vehicle
    ).filter(
        Vehicle.vehicle_type.ilike("%car%")
    ).count()

    motorcycles = db.query(
        Vehicle
    ).filter(
        Vehicle.vehicle_type.ilike("%motorcycle%")
    ).count()

    buses = db.query(
        Vehicle
    ).filter(
        Vehicle.vehicle_type.ilike("%bus%")
    ).count()

    trucks = db.query(
        Vehicle
    ).filter(
        Vehicle.vehicle_type.ilike("%truck%")
    ).count()

    total_violations = db.query(
        Violation
    ).count()

    total_accidents = db.query(
        Accident
    ).count()

    return {
        "total_vehicles": total_vehicles,
        "cars": cars,
        "motorcycles": motorcycles,
        "buses": buses,
        "trucks": trucks,
        "total_violations": total_violations,
        "total_accidents": total_accidents
    }