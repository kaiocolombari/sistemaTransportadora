from fastapi import APIRouter, Depends
from typing import List
from models.schemas import Vehicle, VehicleCreate
from services.vehicle_service import create_vehicle, list_vehicles, update_vehicle, delete_vehicle
from auth.auth import authenticate_user

router = APIRouter()

@router.post("/vehicles", response_model=Vehicle)
def create_vehicle_endpoint(vehicle: VehicleCreate, user: dict = Depends(authenticate_user)):
    return create_vehicle(vehicle)

@router.get("/vehicles", response_model=List[Vehicle])
def list_vehicles_endpoint(user: dict = Depends(authenticate_user)):
    return list_vehicles()

@router.put("/vehicles/{vehicle_id}", response_model=Vehicle)
def update_vehicle_endpoint(vehicle_id: str, vehicle: VehicleCreate, user: dict = Depends(authenticate_user)):
    return update_vehicle(vehicle_id, vehicle)

@router.delete("/vehicles/{vehicle_id}")
def delete_vehicle_endpoint(vehicle_id: str, user: dict = Depends(authenticate_user)):
    return delete_vehicle(vehicle_id)