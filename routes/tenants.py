
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from models.tenants import Tenant
from schemas.tenants import TenantCreate, TenantResponse

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


# 1. CREATE TENANT
@router.post("/", response_model=TenantResponse)
def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):
    existing_tenant = db.query(Tenant).filter(
        Tenant.email == tenant.email
    ).first()

    if existing_tenant:
        raise HTTPException(
            status_code=400,
            detail="Tenant email already exists"
        )

    new_tenant = Tenant(**tenant.model_dump())

    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)

    return new_tenant


# 2. GET ALL TENANTS
@router.get("/", response_model=list[TenantResponse])
def get_all_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    return tenants


# 3. GET TENANT BY ID
@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return tenant


# 4. UPDATE TENANT
@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: int,
    tenant_data: TenantCreate,
    db: Session = Depends(get_db)
):
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    existing_email = db.query(Tenant).filter(
        Tenant.email == tenant_data.email,
        Tenant.id != tenant_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Tenant email already exists"
        )

    update_data = tenant_data.model_dump()

    for key, value in update_data.items():
        setattr(tenant, key, value)

    db.commit()
    db.refresh(tenant)

    return tenant


# 5. DELETE TENANT
@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    db.delete(tenant)
    db.commit()

    return {
        "message": "Tenant deleted successfully"
    }
