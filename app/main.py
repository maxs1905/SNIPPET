import logging
import logging.config
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logger import LOGGING_CONFIG
from app.api.routes import auth, snippets
from app.db.session import database
from app.db.init_db import init_db

# Применение конфигурации логов
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Code Snippet API")

# Middleware для глобальной обработки ошибок
@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        logger.warning(f"{request.method} {request.url} -> {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )
    except Exception as e:
        logger.error(f"{request.method} {request.url} -> 500: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )

# Обработчик исключений по умолчанию
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"{request.method} {request.url} -> Unhandled error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "Something went wrong"})

# Обработчик HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"{request.method} {request.url} -> HTTP error: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(snippets.router, prefix="/snippets", tags=["Snippets"])

@app.on_event("startup")
async def startup():
    logger.info("Connecting to database...")
    await database.connect()
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnecting from database...")
    await database.disconnect()