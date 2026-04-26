from fastapi import FastAPI

from app.core.config import settings
from app.routers import admin, auth, users

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
