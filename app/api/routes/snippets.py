from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_user
from app.schemas.snippet import SnippetCreate, SnippetOut, SnippetUpdate
from app.services.snippet_service import (
    create_snippet, get_snippet_by_uuid, update_snippet, delete_snippet
)
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=SnippetOut)
async def create(snippet: SnippetCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_snippet(db, snippet, owner_id=current_user.id)

@router.get("/{uuid}", response_model=SnippetOut)
async def get_by_uuid(uuid: str, db: AsyncSession = Depends(get_db)):
    snippet = await get_snippet_by_uuid(db, uuid)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet

@router.put("/{id}", response_model=SnippetOut)
async def update(id: int, snippet_in: SnippetUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    snippet = await update_snippet(db, id, snippet_in)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    if snippet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return snippet

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    snippet = await delete_snippet(db, id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    if snippet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"detail": "Snippet deleted"}