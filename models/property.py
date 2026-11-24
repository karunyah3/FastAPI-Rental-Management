
from sqlalchemy import (
    Column, Integer, String, Text, Numeric,
    DateTime, ForeignKey, CheckConstraint, func
)
from database.connection import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, ForeignKey("owners.id"),
                      nullable=False)

    title = Column(String(150), nullable=False)
    address = Column(Text, nullable=False)
    property_type = Column(String(50), nullable=False)
    monthly_rent = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False, default="Available")

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("monthly_rent > 0",
                        name="check_property_rent"),
    )
