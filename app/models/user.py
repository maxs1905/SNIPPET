from sqlalchemy import Column, String, Enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import database
from enum import Enum as PyEnum

class Role(PyEnum):
    user = "user"
    admin = "admin"

class User(database):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.user)

    snippets = relationship("Snippet", back_populates="owner")
