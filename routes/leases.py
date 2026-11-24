
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database.connection import get_db
from models.lease import Lease
from models.property import Property
from models.tenants import Tenant

from schemas.lease import (
    LeaseCreate,
    LeaseUpdate,
    LeaseResponse
)

router = APIRouter(prefix="/leases", tags=["Leases"])


# UPDATE PROPERTY STATUS
def update_property_status(db: Session, property_id: int):
    property = db.query(Property).filter(
        Property.id == property_id
    ).first()

    if not property:
        return

    today = date.today()

    current_lease = db.query(Lease).filter(
        Lease.property_id == property_id,
        Lease.status == "Active",
        Lease.start_date <= today,
        Lease.end_date >= today
    ).first()

    if current_lease:
        property.status = "Rented"
    else:
        property.status = "Available"


# CREATE LEASE
@router.post("/", response_model=LeaseResponse, status_code=201)
def create_lease(data: LeaseCreate, db: Session = Depends(get_db)):

    property = db.query(Property).filter(
        Property.id == data.property_id
    ).first()

    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    tenant = db.query(Tenant).filter(
        Tenant.id == data.tenant_id
    ).first()

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    if data.end_date <= data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    if data.monthly_rent <= 0:
        raise HTTPException(
            status_code=400,
            detail="Monthly rent must be greater than zero"
        )

    if data.status == "Active":
        overlapping_lease = db.query(Lease).filter(
            Lease.property_id == data.property_id,
            Lease.status == "Active",
            Lease.start_date <= data.end_date,
            Lease.end_date >= data.start_date
        ).first()

        if overlapping_lease:
            raise HTTPException(
                status_code=400,
                detail="Property already has an overlapping active lease"
            )

    new_lease = Lease(**data.model_dump())

    db.add(new_lease)
    db.flush()

    update_property_status(db, new_lease.property_id)

    db.commit()
    db.refresh(new_lease)

    return new_lease


# READ ALL LEASES
@router.get("/", response_model=list[LeaseResponse])
def get_leases(db: Session = Depends(get_db)):
    return db.query(Lease).all()


# READ LEASE BY ID
@router.get("/{lease_id}", response_model=LeaseResponse)
def get_lease(lease_id: int, db: Session = Depends(get_db)):

    lease = db.query(Lease).filter(
        Lease.id == lease_id
    ).first()

    if not lease:
        raise HTTPException(status_code=404, detail="Lease not found")

    return lease


# UPDATE LEASE
@router.put("/{lease_id}", response_model=LeaseResponse)
def update_lease(
    lease_id: int,
    data: LeaseUpdate,
    db: Session = Depends(get_db)
):

    lease = db.query(Lease).filter(
        Lease.id == lease_id
    ).first()

    if not lease:
        raise HTTPException(status_code=404, detail="Lease not found")

    update_data = data.model_dump(exclude_unset=True)

    old_property_id = lease.property_id

    property_id = update_data.get("property_id", lease.property_id)
    tenant_id = update_data.get("tenant_id", lease.tenant_id)
    start_date = update_data.get("start_date", lease.start_date)
    end_date = update_data.get("end_date", lease.end_date)
    monthly_rent = update_data.get("monthly_rent", lease.monthly_rent)
    status = update_data.get("status", lease.status)

    if not db.query(Property).filter(
        Property.id == property_id
    ).first():
        raise HTTPException(status_code=404, detail="Property not found")

    if not db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first():
        raise HTTPException(status_code=404, detail="Tenant not found")

    if end_date <= start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    if monthly_rent <= 0:
        raise HTTPException(
            status_code=400,
            detail="Monthly rent must be greater than zero"
        )

    if status == "Active":
        overlapping_lease = db.query(Lease).filter(
            Lease.property_id == property_id,
            Lease.status == "Active",
            Lease.id != lease_id,
            Lease.start_date <= end_date,
            Lease.end_date >= start_date
        ).first()

        if overlapping_lease:
            raise HTTPException(
                status_code=400,
                detail="Property already has an overlapping active lease"
            )

    for key, value in update_data.items():
        setattr(lease, key, value)

    db.flush()

    update_property_status(db, old_property_id)

    if property_id != old_property_id:
        update_property_status(db, property_id)

    db.commit()
    db.refresh(lease)

    return lease


# DELETE LEASE
@router.delete("/{lease_id}")
def delete_lease(lease_id: int, db: Session = Depends(get_db)):

    lease = db.query(Lease).filter(
        Lease.id == lease_id
    ).first()

    if not lease:
        raise HTTPException(status_code=404, detail="Lease not found")

    property_id = lease.property_id

    db.delete(lease)
    db.flush()

    update_property_status(db, property_id)

    db.commit()

    return {"message": "Lease deleted successfully"}

# EXPIRE OLD LEASES
def expire_old_leases(db: Session):

    today = date.today()

    old_leases = db.query(Lease).filter(
        Lease.status == "Active",
        Lease.end_date < today
    ).all()

    affected_properties = set()

    for lease in old_leases:
        lease.status = "Expired"
        affected_properties.add(lease.property_id)

    for property_id in affected_properties:
        update_property_status(db, property_id)

    db.commit()

    return len(old_leases)


# MANUAL LEASE EXPIRATION API
@router.post("/expire-old")
def expire_old_leases_api(db: Session = Depends(get_db)):

    count = expire_old_leases(db)

    return {
        "message": "Expired leases updated successfully",
        "expired_count": count
    }
