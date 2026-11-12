from fastapi import FastAPI
from app.config import Settings
from app.routers import items

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