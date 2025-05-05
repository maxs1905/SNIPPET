from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    code = Column(String)
    language = Column(String)
    is_public = Column(Boolean, default=True)
    owner_id = Column(Integer, index=True)
    uuid = Column(String, unique=True)