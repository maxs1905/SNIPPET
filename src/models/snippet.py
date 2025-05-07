from  datetime import datetime

from sqlalchemy import String, Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base


class ShortedUrl(Base):
    tablename = "url"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    origin = Column(String(256))
    shorted_url = Column(String(256), unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable= False)

    owner = relationship("User", backref="snippets")