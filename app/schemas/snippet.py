from pydantic import BaseModel
from typing import Optional

class SnippetBase(BaseModel):
    title: str
    code: str
    is_public: bool = True

class SnippetCreate(SnippetBase):
    language: Optional[str] = "python"

class SnippetUpdate(SnippetBase):
    title: Optional[str]
    code: Optional[str]
    language: Optional[str]
    is_public: Optional[bool]

class SnippetOut(SnippetBase):
    id: int
    uuid: str
    owner_id: int

    class Config:
        orm_mode = True