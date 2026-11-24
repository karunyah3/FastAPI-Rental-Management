
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Literal


class LeaseCreate(BaseModel):
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_rent: Decimal
    status: Literal["Active", "Terminated", "Expired"] = "Active"


class LeaseUpdate(BaseModel):
    property_id: Optional[int] = None
    tenant_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    monthly_rent: Optional[Decimal] = None
    status: Optional[Literal["Active", "Terminated", "Expired"]] = None


class LeaseResponse(BaseModel):
    id: int
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_rent: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
