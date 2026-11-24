from pydantic import BaseModel, EmailStr, ConfigDict

class TenantCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class TenantResponse(TenantCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)