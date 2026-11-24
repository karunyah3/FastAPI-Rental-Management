from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class PropertyCreate(BaseModel):
    owner_id: int
    title: str
    address: str
    property_type: str
    monthly_rent: Decimal
    status: str = "Available"

class PropertyResponse(PropertyCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)