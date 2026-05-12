from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_complaint_service
from app.models.schemas import AnalyticsResponse, ComplaintCreate, ComplaintListResponse, ComplaintResponse
from app.services.complaints import ComplaintService

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/complaints", response_model=ComplaintResponse, status_code=201)
async def submit_complaint(
    payload: ComplaintCreate,
    service: Annotated[ComplaintService, Depends(get_complaint_service)],
) -> ComplaintResponse:
    return await service.submit(payload)


@router.get("/complaints", response_model=ComplaintListResponse)
async def list_complaints(
    service: Annotated[ComplaintService, Depends(get_complaint_service)],
    limit: int = 25,
) -> ComplaintListResponse:
    return ComplaintListResponse(complaints=await service.list_recent(limit=limit))


@router.get("/analytics", response_model=AnalyticsResponse)
async def analytics(service: Annotated[ComplaintService, Depends(get_complaint_service)]) -> AnalyticsResponse:
    return await service.analytics()

