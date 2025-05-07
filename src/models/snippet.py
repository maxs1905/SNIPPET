from  datetime import datetime

from sqlalchemy import String, Column, Integer, TIMESTAMP

from src.db.base import Base


class ShortedUrl(Base):
    tablename = "url"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    origin = Column(String(256))
    shorted_url = Column(String(256), unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)