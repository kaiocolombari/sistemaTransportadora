from fastapi import APIRouter, Depends
from services.dashboard_service import get_dashboard_stats
from auth.auth import authenticate_user

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats_endpoint(user: dict = Depends(authenticate_user)):
    return get_dashboard_stats()