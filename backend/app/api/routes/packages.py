"""
Package 라우터.

GET /api/packages/{package_name}/tags  - Package 하위 Tag 목록
"""
from typing import List

from fastapi import APIRouter

from app.core.exceptions import ResourceNotFoundError
from app.models.schemas import ErrorResponse, TagSummary
from app.services.hierarchy_service import listTagsByPackage

router = APIRouter(prefix="/api/packages", tags=["packages"])


@router.get(
    "/{packageName}/tags",
    response_model=List[TagSummary],
    summary="특정 Package 하위 Tag 목록",
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def listPackageTagsRoute(packageName: str) -> List[TagSummary]:
    """주어진 Package 에 속한 Tag 요약 목록 반환."""
    tags = listTagsByPackage(packageName)
    if not tags:
        raise ResourceNotFoundError(
            f"Package '{packageName}' not found or has no tags",
            code="PACKAGE_NOT_FOUND",
        )
    return tags
