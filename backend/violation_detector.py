import random


def detect_violations(vehicle_analysis):

    violations = []

    vehicle_types = [
        "car",
        "motorcycle",
        "bus",
        "truck"
    ]

    violation_types = [
        "Signal Jumping",
        "Wrong Parking",
        "Over Speeding",
        "Lane Violation"
    ]

    for vehicle_type in vehicle_types:

        count = vehicle_analysis.get(
            vehicle_type,
            0
        )

        for i in range(count):

            if random.random() < 0.25:

                violations.append(
                    {
                        "vehicle_number": f"{vehicle_type.upper()}-{i+1}",
                        "violation_type": random.choice(
                            violation_types
                        ),
                        "location": "Guardian Zone"
                    }
                )

    return violations