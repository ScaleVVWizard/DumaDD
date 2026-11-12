import logging
import time
from fastapi import FastAPI, Request
from app.config import Settings
from app.routers import items

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("app")

settings = Settings()
app = FastAPI(
    title=settings.app_name,
    description="Лабораторная работа по FastAPI",
    version="1.0.0",
    contact={
        "name": "Студент",
        "email": settings.admin_email,
    }
)
app.include_router(items.router)

# Middleware для логирования каждого запроса
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.2f} ms)")
    return response

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/info")
def get_info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_page": settings.items_per_page,
    }