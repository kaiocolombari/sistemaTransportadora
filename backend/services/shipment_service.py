from fastapi import HTTPException
import uuid
from datetime import datetime
from models.data import shipments
from models.schemas import Shipment, ShipmentCreate, ShipmentUpdate

def create_shipment(shipment: ShipmentCreate):
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

def list_shipments():
    return shipments

def get_shipment(shipment_id: str):
    for shipment in shipments:
        if shipment.id == shipment_id:
            return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")

def update_shipment_status(shipment_id: str, update: ShipmentUpdate):
    for shipment in shipments:
        if shipment.id == shipment_id:
            shipment.status = update.status
            return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")