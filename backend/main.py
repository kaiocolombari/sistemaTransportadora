from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import secrets

app = FastAPI(title="Transportadora API", description="API for transportation system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

users = [
    {"id": "1", "username": "admin", "password": "admin123", "role": "admin"},
    {"id": "2", "username": "driver", "password": "driver123", "role": "driver"}
]
tokens = {}

shipments = []
vehicles = []
clients = []

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

def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens[token]

@app.post("/login")
def login(request: LoginRequest):
    for user in users:
        if user["username"] == request.username and user["password"] == request.password:
            token = secrets.token_hex(32)
            tokens[token] = user
            return {"token": token, "user": User(id=user["id"], username=user["username"], role=user["role"])}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token in tokens:
        del tokens[token]
    return {"message": "Logged out"}

# Vehicles CRUD
@app.post("/vehicles", response_model=Vehicle)
def create_vehicle(vehicle: VehicleCreate, user: dict = Depends(authenticate_user)):
    new_vehicle = Vehicle(
        id=str(uuid.uuid4()),
        license_plate=vehicle.license_plate,
        model=vehicle.model,
        capacity=vehicle.capacity
    )
    vehicles.append(new_vehicle)
    return new_vehicle

@app.get("/vehicles", response_model=List[Vehicle])
def list_vehicles(user: dict = Depends(authenticate_user)):
    return vehicles

@app.put("/vehicles/{vehicle_id}", response_model=Vehicle)
def update_vehicle(vehicle_id: str, vehicle: VehicleCreate, user: dict = Depends(authenticate_user)):
    for v in vehicles:
        if v.id == vehicle_id:
            v.license_plate = vehicle.license_plate
            v.model = vehicle.model
            v.capacity = vehicle.capacity
            return v
    raise HTTPException(status_code=404, detail="Vehicle not found")

@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: str, user: dict = Depends(authenticate_user)):
    for i, v in enumerate(vehicles):
        if v.id == vehicle_id:
            del vehicles[i]
            return {"message": "Vehicle deleted"}
    raise HTTPException(status_code=404, detail="Vehicle not found")

# Clients CRUD
@app.post("/clients", response_model=Client)
def create_client(client: ClientCreate, user: dict = Depends(authenticate_user)):
    new_client = Client(
        id=str(uuid.uuid4()),
        name=client.name,
        email=client.email,
        phone=client.phone
    )
    clients.append(new_client)
    return new_client

@app.get("/clients", response_model=List[Client])
def list_clients(user: dict = Depends(authenticate_user)):
    return clients

@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: str, client: ClientCreate, user: dict = Depends(authenticate_user)):
    for c in clients:
        if c.id == client_id:
            c.name = client.name
            c.email = client.email
            c.phone = client.phone
            return c
    raise HTTPException(status_code=404, detail="Client not found")

@app.delete("/clients/{client_id}")
def delete_client(client_id: str, user: dict = Depends(authenticate_user)):
    for i, c in enumerate(clients):
        if c.id == client_id:
            del clients[i]
            return {"message": "Client deleted"}
    raise HTTPException(status_code=404, detail="Client not found")

@app.post("/shipments", response_model=Shipment)
def create_shipment(shipment: ShipmentCreate, user: dict = Depends(authenticate_user)):
    new_shipment = Shipment(
        id=str(uuid.uuid4()),
        origin=shipment.origin,
        destination=shipment.destination,
        date_created=datetime.now(),
        client_id=shipment.client_id,
        vehicle_id=shipment.vehicle_id
    )
    shipments.append(new_shipment)
    return new_shipment

@app.get("/shipments", response_model=List[Shipment])
def list_shipments(user: dict = Depends(authenticate_user)):
    return shipments

@app.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: str, user: dict = Depends(authenticate_user)):
    for shipment in shipments:
        if shipment.id == shipment_id:
            return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")

@app.put("/shipments/{shipment_id}", response_model=Shipment)
def update_shipment_status(shipment_id: str, update: ShipmentUpdate, user: dict = Depends(authenticate_user)):
    for shipment in shipments:
        if shipment.id == shipment_id:
            shipment.status = update.status
            return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")

@app.get("/dashboard")
def get_dashboard_stats(user: dict = Depends(authenticate_user)):
    total_shipments = len(shipments)
    pending = len([s for s in shipments if s.status == "Pending"])
    in_transit = len([s for s in shipments if s.status == "In Transit"])
    delivered = len([s for s in shipments if s.status == "Delivered"])
    total_vehicles = len(vehicles)
    available_vehicles = len([v for v in vehicles if v.status == "Available"])
    total_clients = len(clients)
    
    return {
        "shipments": {
            "total": total_shipments,
            "pending": pending,
            "in_transit": in_transit,
            "delivered": delivered
        },
        "vehicles": {
            "total": total_vehicles,
            "available": available_vehicles
        },
        "clients": {
            "total": total_clients
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)