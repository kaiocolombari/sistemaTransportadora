from fastapi import APIRouter, Depends
from typing import List
from models.schemas import Client, ClientCreate
from services.client_service import create_client, list_clients, update_client, delete_client
from auth.auth import authenticate_user

router = APIRouter()

@router.post("/clients", response_model=Client)
def create_client_endpoint(client: ClientCreate, user: dict = Depends(authenticate_user)):
    return create_client(client)

@router.get("/clients", response_model=List[Client])
def list_clients_endpoint(user: dict = Depends(authenticate_user)):
    return list_clients()

@router.put("/clients/{client_id}", response_model=Client)
def update_client_endpoint(client_id: str, client: ClientCreate, user: dict = Depends(authenticate_user)):
    return update_client(client_id, client)

@router.delete("/clients/{client_id}")
def delete_client_endpoint(client_id: str, user: dict = Depends(authenticate_user)):
    return delete_client(client_id)