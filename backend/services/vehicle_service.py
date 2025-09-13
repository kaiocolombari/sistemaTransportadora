from fastapi import HTTPException
import uuid
from models.data import vehicles
from models.schemas import Vehicle, VehicleCreate

def create_vehicle(vehicle: VehicleCreate):
    new_vehicle = Vehicle(
        id=str(uuid.uuid4()),
        license_plate=vehicle.license_plate,
        model=vehicle.model,
        capacity=vehicle.capacity
    )
    vehicles.append(new_vehicle)
    return new_vehicle

def list_vehicles():
    return vehicles

def update_vehicle(vehicle_id: str, vehicle: VehicleCreate):
    for v in vehicles:
        if v.id == vehicle_id:
            v.license_plate = vehicle.license_plate
            v.model = vehicle.model
            v.capacity = vehicle.capacity
            return v
    raise HTTPException(status_code=404, detail="Vehicle not found")

def delete_vehicle(vehicle_id: str):
    for i, v in enumerate(vehicles):
        if v.id == vehicle_id:
            del vehicles[i]
            return {"message": "Vehicle deleted"}
    raise HTTPException(status_code=404, detail="Vehicle not found")