from sqlalchemy.future import select
from fastapi import HTTPException
from src.db.db import db_dependency
from src.models.snippet import ShortedUrl
from src.models.user import User

# Получение URL по ID
async def get_url_by_id(db: db_dependency, url_id: int):
    result = await db.execute(select(ShortedUrl).filter(ShortedUrl.id == url_id))
    return result.scalars().first()

# Получение URL по короткой ссылке
async def get_url_by_shorted_url(db: db_dependency, shorted_url: str):
    result = await db.execute(select(ShortedUrl).filter(ShortedUrl.shorted_url == shorted_url))
    return result.scalars().first()

# Получение списка URL
async def get_urls(db: db_dependency, skip: int = 0, limit: int = 10):
    result = await db.execute(select(ShortedUrl).offset(skip).limit(limit))
    return result.scalars().all()

# Создание нового сниппета
async def create_url(db: db_dependency, origin: str, shorted_url: str, owner_id: int):
    db_url = ShortedUrl(origin=origin, shorted_url=shorted_url, owner_id=owner_id)
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url

# Обновление сниппета
async def update_url(db: db_dependency, url_id: int, origin: str, shorted_url: str, current_user_id: int):
    db_url = await get_url_by_id(db, url_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="Snippet not found")

    # Проверяем, что пользователь имеет доступ к изменению этого сниппета
    if db_url.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")

    db_url.origin = origin
    db_url.shorted_url = shorted_url
    await db.commit()
    await db.refresh(db_url)
    return db_url

# Удаление сниппета
async def delete_url(db: db_dependency, url_id: int, current_user_id: int):
    db_url = await get_url_by_id(db, url_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="Snippet not found")

    # Проверяем, что пользователь имеет доступ к удалению этого сниппета
    if db_url.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")

    await db.delete(db_url)
    await db.commit()
    return db_url