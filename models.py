from sqlalchemy import Column, Integer, JSON, DateTime, Boolean, ForeignKey, String, Table
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from database import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata, 
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE")
    ),
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    
class UploadedRecords(Base):
    __tablename__ = "upload_records"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow())

