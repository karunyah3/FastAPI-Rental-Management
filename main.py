
from fastapi import FastAPI
from database.connection import Base, engine
from models.owner import Owner
from models.property import Property
from models.tenant import Tenant
from models.lease import Lease
from routes import owners,properties

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Property Rental System API")

app.include_router(owners.router)
app.include_router(properties.router)


@app.get("/")
def home():
    return {"message": "Property Rental System API is running"}
