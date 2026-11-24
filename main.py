from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database.connection import Base, engine
from models.owner import Owner
from models.property import Property
from models.tenants import Tenant
from models.lease import Lease
from routes import owners, properties, tenants, leases
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Property Rental System API")

app.include_router(owners.router)
app.include_router(properties.router)
app.include_router(tenants.router)
app.include_router(leases.router)
@app.get("/")
def home():
    return {"message": "Property Rental System API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)