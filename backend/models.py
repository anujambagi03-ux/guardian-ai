from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String, unique=True)
    vehicle_type = Column(String)
    detection_time = Column(DateTime, default=datetime.utcnow)


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String)
    violation_type = Column(String)
    location = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Accident(Base):
    __tablename__ = "accidents"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)