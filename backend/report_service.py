from models import Vehicle
from models import Violation
from models import Accident


def vehicle_report(db):

    vehicles = db.query(Vehicle).all()

    result = []

    for vehicle in vehicles:
        result.append({
            "id": vehicle.id,
            "vehicle_number": vehicle.vehicle_number,
            "vehicle_type": vehicle.vehicle_type,
            "detection_time": str(vehicle.detection_time)
        })

    return result


def violation_report(db):

    violations = db.query(Violation).all()

    result = []

    for violation in violations:
        result.append({
            "id": violation.id,
            "vehicle_number": violation.vehicle_number,
            "violation_type": violation.violation_type,
            "location": violation.location,
            "timestamp": str(violation.timestamp)
        })

    return result


def accident_report(db):

    accidents = db.query(Accident).all()

    result = []

    for accident in accidents:
        result.append({
            "id": accident.id,
            "location": accident.location,
            "severity": accident.severity,
            "timestamp": str(accident.timestamp)
        })

    return result


def summary_report(db):

    total_vehicles = db.query(Vehicle).count()
    total_violations = db.query(Violation).count()
    total_accidents = db.query(Accident).count()

    return {
        "total_vehicles": total_vehicles,
        "total_violations": total_violations,
        "total_accidents": total_accidents
    }