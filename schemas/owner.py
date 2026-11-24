from pydantic import BaseModel, EmailStr, ConfigDict

class OwnerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class OwnerResponse(OwnerCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
    