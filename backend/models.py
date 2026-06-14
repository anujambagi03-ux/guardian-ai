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