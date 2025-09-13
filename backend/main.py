from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.vehicle_routes import router as vehicle_router
from routes.client_routes import router as client_router
from routes.shipment_routes import router as shipment_router
from routes.dashboard_routes import router as dashboard_router

app = FastAPI(title="Transportadora API", description="API for transportation system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(vehicle_router)
app.include_router(client_router)
app.include_router(shipment_router)
app.include_router(dashboard_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)