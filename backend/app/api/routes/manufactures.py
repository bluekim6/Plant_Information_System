"""
Manufacture 라우터.

GET /api/manufactures                       - 전체 제조사 목록
GET /api/manufactures/{manufacture_name}    - 제조사 상세 (popup 용)
"""
from typing import List

from fastapi import APIRouter

from app.core.exceptions import ResourceNotFoundError
from app.models.schemas import ErrorResponse, ManufactureDetail
from app.repositories.manufacture_repository import findAllManufactures
from app.services.manufacture_service import getManufactureDetail

router = APIRouter(prefix="/api/manufactures", tags=["manufactures"])


@router.get(
    "",
    response_model=List[ManufactureDetail],
    summary="전체 제조사 목록",
    responses={503: {"model": ErrorResponse}},
)
def listManufacturesRoute() -> List[ManufactureDetail]:
    return findAllManufactures()


@router.get(
    "/{manufactureName}",
    response_model=ManufactureDetail,
    summary="제조사 상세 (popup)",
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def getManufactureRoute(manufactureName: str) -> ManufactureDetail:
    detail = getManufactureDetail(manufactureName)
    if detail is None:
        raise ResourceNotFoundError(
            f"Manufacture '{manufactureName}' not found",
            code="MANUFACTURE_NOT_FOUND",
        )
    return detail
