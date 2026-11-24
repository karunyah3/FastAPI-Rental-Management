
from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime,
    ForeignKey, CheckConstraint, func
)
from database.connection import Base


class Lease(Base):
    __tablename__ = "leases"

    id = Column(Integer, primary_key=True, index=True)

    property_id = Column(Integer, ForeignKey("properties.id"),
                         nullable=False)

    tenant_id = Column(Integer, ForeignKey("tenants.id"),
                       nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_rent = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False, default="Active")

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("monthly_rent > 0",
                        name="check_lease_rent"),
        CheckConstraint("end_date > start_date",
                        name="check_lease_dates"),
    )
