from pydantic import BaseModel


class VehicleCreate(BaseModel):
    vehicle_number: str
    vehicle_type: str


class ViolationCreate(BaseModel):
    vehicle_number: str
    violation_type: str
    location: str


class AccidentCreate(BaseModel):
    location: str
    severity: str


class AlertCreate(BaseModel):
    alert_type: str
    severity: str
    message: str