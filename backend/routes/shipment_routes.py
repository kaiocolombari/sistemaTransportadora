from fastapi import APIRouter, Depends
from typing import List
from models.schemas import Shipment, ShipmentCreate, ShipmentUpdate
from services.shipment_service import create_shipment, list_shipments, get_shipment, update_shipment_status
from auth.auth import authenticate_user

router = APIRouter()

@router.post("/shipments", response_model=Shipment)
def create_shipment_endpoint(shipment: ShipmentCreate, user: dict = Depends(authenticate_user)):
    return create_shipment(shipment)

@router.get("/shipments", response_model=List[Shipment])
def list_shipments_endpoint(user: dict = Depends(authenticate_user)):
    return list_shipments()

@router.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment_endpoint(shipment_id: str, user: dict = Depends(authenticate_user)):
    return get_shipment(shipment_id)

@router.put("/shipments/{shipment_id}", response_model=Shipment)
def update_shipment_status_endpoint(shipment_id: str, update: ShipmentUpdate, user: dict = Depends(authenticate_user)):
    return update_shipment_status(shipment_id, update)