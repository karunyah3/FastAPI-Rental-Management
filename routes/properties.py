
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import SessionLocal
from models.property import Property
from models.owner import Owner
from schemas.property import PropertyCreate, PropertyResponse

router = APIRouter(prefix="/properties", tags=["Properties"])


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE property
@router.post("/", response_model=PropertyResponse, status_code=201)
def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    # Check whether owner exists
    owner = db.query(Owner).filter(
        Owner.id == property_data.owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    new_property = Property(**property_data.model_dump())

    db.add(new_property)
    db.commit()
    db.refresh(new_property)

    return new_property

# READ all properties
@router.get("/", response_model=list[PropertyResponse])
def get_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()


# READ one property by ID
@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property = db.query(Property).filter(
        Property.id == property_id
    ).first()

    if not property:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return property

# UPDATE property
@router.put("/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    property = db.query(Property).filter(
        Property.id == property_id
    ).first()

    if not property:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    # Check whether the new owner exists
    owner = db.query(Owner).filter(
        Owner.id == property_data.owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    for key, value in property_data.model_dump().items():
        setattr(property, key, value)

    db.commit()
    db.refresh(property)

    return property

# DELETE property
@router.delete("/{property_id}")
def delete_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property = db.query(Property).filter(
        Property.id == property_id
    ).first()

    if not property:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    db.delete(property)
    db.commit()

    return {"message": "Property deleted successfully"}
