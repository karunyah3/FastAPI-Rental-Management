
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import SessionLocal
from models.owner import Owner
from schemas.owner import OwnerCreate, OwnerResponse

router = APIRouter(prefix="/owners", tags=["Owners"])

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE owner
@router.post("/", response_model=OwnerResponse, status_code=201)
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    existing = db.query(Owner).filter(Owner.email == owner.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_owner = Owner(**owner.model_dump())
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return new_owner

# READ all owners
@router.get("/", response_model=list[OwnerResponse])
def get_owners(db: Session = Depends(get_db)):
    return db.query(Owner).all()

# READ one owner
@router.get("/{owner_id}", response_model=OwnerResponse)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner

# UPDATE owner
@router.put("/{owner_id}", response_model=OwnerResponse)
def update_owner(owner_id: int, data: OwnerCreate, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    if data.email != owner.email:
        existing = db.query(Owner).filter(Owner.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    for key, value in data.model_dump().items():
        setattr(owner, key, value)

    db.commit()
    db.refresh(owner)
    return owner

# DELETE owner
@router.delete("/{owner_id}")
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    db.delete(owner)
    db.commit()
    return {"message": "Owner deleted successfully"}

# READ one owner by ID
@router.get("/{owner_id}", response_model=OwnerResponse)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    return owner

# UPDATE owner
@router.put("/{owner_id}", response_model=OwnerResponse)
def update_owner(
    owner_id: int,
    owner_data: OwnerCreate,
    db: Session = Depends(get_db)
):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    existing = db.query(Owner).filter(
        Owner.email == owner_data.email,
        Owner.id != owner_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    for key, value in owner_data.model_dump().items():
        setattr(owner, key, value)

    db.commit()
    db.refresh(owner)

    return owner



# DELETE owner
@router.delete("/{owner_id}")
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    db.delete(owner)
    db.commit()

    return {"message": "Owner deleted successfully"}
