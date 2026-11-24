from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date

class LeaseCreate(BaseModel):
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_rent: Decimal
    status: str = "Active"

class LeaseResponse(LeaseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)