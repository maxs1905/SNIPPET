from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID

class SnippetBase(BaseModel):
    title: str
    code: str
    is_public: bool = True

class SnippetCreate(SnippetBase):
    title: str
    code: str
    language: Optional[str] = "python"

class SnippetUpdate(SnippetBase):
    title: Optional[str]
    code: Optional[str]
    language: Optional[str]
    is_public: Optional[bool]

class SnippetOut(SnippetBase):
    id: int
    title: str
    code: str
    language: str
    is_public: bool
    uuid: str
    owner_id: int

    class Config:
        orm_mode = True
