from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String, unique=True)
    vehicle_type = Column(String)

    detection_time = Column(
        DateTime,
        default=datetime.utcnow
    )


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_number = Column(String)

    violation_type = Column(String)

    location = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


class Accident(Base):
    __tablename__ = "accidents"

    id = Column(Integer, primary_key=True, index=True)

    location = Column(String)

    severity = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    alert_type = Column(String)

    severity = Column(String)

    message = Column(String)

    status = Column(
        String,
        default="ACTIVE"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class DetectionFrame(Base):
    __tablename__ = "detection_frames"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    frame_id = Column(String)

    vehicle_count = Column(Integer)

    cars = Column(
        Integer,
        default=0
    )

    trucks = Column(
        Integer,
        default=0
    )

    buses = Column(
        Integer,
        default=0
    )

    motorcycles = Column(
        Integer,
        default=0
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


class TrackedVehicle(Base):
    __tablename__ = "tracked_vehicles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    tracking_id = Column(
        String,
        unique=True
    )

    vehicle_type = Column(String)

    confidence = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class TrafficFlow(Base):
    __tablename__ = "traffic_flow"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    total_vehicles = Column(
        Integer,
        default=0
    )

    cars = Column(
        Integer,
        default=0
    )

    trucks = Column(
        Integer,
        default=0
    )

    buses = Column(
        Integer,
        default=0
    )

    motorcycles = Column(
        Integer,
        default=0
    )

    traffic_status = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


class NearMissEvent(Base):
    __tablename__ = "near_miss_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_a = Column(String)

    vehicle_b = Column(String)

    distance = Column(Integer)

    risk_level = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


class AccidentRisk(Base):
    __tablename__ = "accident_risk"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    risk_score = Column(Integer)

    risk_level = Column(String)

    traffic_status = Column(String)

    near_miss_count = Column(Integer)

    recommendation = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )
class EmergencyResponse(Base):
    __tablename__ = "emergency_responses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    emergency_level = Column(String)

    response_action = Column(String)

    estimated_time = Column(Integer)

    risk_score = Column(Integer)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    ) 
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String,
        unique=True
    )

    risk_level = Column(String)

    emergency_level = Column(String)

    priority = Column(String)

    assigned_team = Column(String)

    status = Column(
        String,
        default="OPEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )   
class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    dispatch_id = Column(
        String,
        unique=True
    )

    incident_id = Column(String)

    vehicle_type = Column(String)

    personnel_count = Column(Integer)

    dispatch_status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
class ResponseTracking(Base):
    __tablename__ = "response_tracking"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    response_id = Column(
        String,
        unique=True
    )

    dispatch_id = Column(String)

    incident_id = Column(String)

    response_status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
class ResolutionCase(Base):
    __tablename__ = "resolution_cases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resolution_id = Column(
        String,
        unique=True
    )

    response_id = Column(String)

    incident_id = Column(String)

    resolution_status = Column(String)

    resolution_notes = Column(String)

    closure_time_minutes = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
class ResourceUnit(Base):
    __tablename__ = "resource_units"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resource_id = Column(
        String,
        unique=True
    )

    resource_type = Column(String)

    availability_status = Column(String)

    current_location = Column(String)

    utilization_score = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
class TrafficPrediction(Base):
    __tablename__ = "traffic_predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    prediction_id = Column(
        String,
        unique=True
    )

    current_traffic = Column(String)

    predicted_traffic = Column(String)

    confidence_score = Column(Integer)

    prediction_window = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )