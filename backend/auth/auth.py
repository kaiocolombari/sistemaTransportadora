from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.data import tokens

security = HTTPBearer()

def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens[token]