from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship
from src.db.base import Base


class User(Base):
    tablename = "user"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(256), unique=True, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    salt = Column(String(1024), nullable=False, unique=True, index=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role", back_populates="users")