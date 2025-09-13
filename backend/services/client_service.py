from fastapi import HTTPException
import uuid
from models.data import clients
from models.schemas import Client, ClientCreate

def create_client(client: ClientCreate):
    new_client = Client(
        id=str(uuid.uuid4()),
        name=client.name,
        email=client.email,
        phone=client.phone
    )
    clients.append(new_client)
    return new_client

def list_clients():
    return clients

def update_client(client_id: str, client: ClientCreate):
    for c in clients:
        if c.id == client_id:
            c.name = client.name
            c.email = client.email
            c.phone = client.phone
            return c
    raise HTTPException(status_code=404, detail="Client not found")

def delete_client(client_id: str):
    for i, c in enumerate(clients):
        if c.id == client_id:
            del clients[i]
            return {"message": "Client deleted"}
    raise HTTPException(status_code=404, detail="Client not found")