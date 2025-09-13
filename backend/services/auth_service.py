from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import secrets
from models.data import users, tokens
from models.schemas import User, LoginRequest

def login(request: LoginRequest):
    for user in users:
        if user["username"] == request.username and user["password"] == request.password:
            token = secrets.token_hex(32)
            tokens[token] = user
            return {"token": token, "user": User(id=user["id"], username=user["username"], role=user["role"])}
    raise HTTPException(status_code=401, detail="Invalid credentials")

def logout(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    if token in tokens:
        del tokens[token]
    return {"message": "Logged out"}