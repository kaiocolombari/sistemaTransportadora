from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: str
    username: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Vehicle(BaseModel):
    id: str
    license_plate: str
    model: str
    capacity: int
    status: str = "Available"

class VehicleCreate(BaseModel):
    license_plate: str
    model: str
    capacity: int

class Client(BaseModel):
    id: str
    name: str
    email: str
    phone: str

class ClientCreate(BaseModel):
    name: str
    email: str
    phone: str

class Shipment(BaseModel):
    id: str
    origin: str
    destination: str
    status: str = "Pending"
    date_created: datetime
    client_id: Optional[str] = None
    vehicle_id: Optional[str] = None

class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    client_id: Optional[str] = None
    vehicle_id: Optional[str] = None

class ShipmentUpdate(BaseModel):
    status: str