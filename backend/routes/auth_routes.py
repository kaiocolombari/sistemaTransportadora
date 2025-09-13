from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from models.schemas import LoginRequest
from services.auth_service import login, logout
from auth.auth import authenticate_user

router = APIRouter()

@router.post("/login")
def login_endpoint(request: LoginRequest):
    return login(request)

@router.post("/logout")
def logout_endpoint(credentials: HTTPAuthorizationCredentials = Depends(authenticate_user)):
    return logout(credentials)