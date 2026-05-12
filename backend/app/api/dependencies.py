from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.settings import Settings, get_settings
from app.services.complaints import ComplaintService


async def get_complaint_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ComplaintService:
    return ComplaintService(session=session, settings=settings)

