import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.snippet import Snippet
from app.schemas.snippet import SnippetCreate, SnippetUpdate

async def create_snippet(db: AsyncSession, snippet_in: SnippetCreate, owner_id: int):
    new_snippet = Snippet(
        title=snippet_in.title,
        code=snippet_in.code,
        language=snippet_in.language,
        is_public=snippet_in.is_public,
        owner_id=owner_id,
        uuid=str(uuid.uuid4())
    )
    db.add(new_snippet)
    await db.commit()
    await db.refresh(new_snippet)
    return new_snippet

async def get_snippet_by_uuid(db: AsyncSession, snippet_uuid: str):
    result = await db.execute(select(Snippet).where(Snippet.uuid == snippet_uuid))
    return result.scalars().first()

async def update_snippet(db: AsyncSession, snippet_id: int, snippet_in: SnippetUpdate):
    result = await db.execute(select(Snippet).where(Snippet.id == snippet_id))
    snippet = result.scalars().first()
    if snippet:
        for key, value in snippet_in.dict(exclude_unset=True).items():
            setattr(snippet, key, value)
        await db.commit()
        await db.refresh(snippet)
    return snippet

async def delete_snippet(db: AsyncSession, snippet_id: int):
    result = await db.execute(select(Snippet).where(Snippet.id == snippet_id))
    snippet = result.scalars().first()
    if snippet:
        await db.delete(snippet)
        await db.commit()
    return snippet