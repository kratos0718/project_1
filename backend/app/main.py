from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config.database import engine
from app.config.settings import get_settings
from app.models.database import Base

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def initialize_database() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
