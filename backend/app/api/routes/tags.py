"""
Tag 라우터.

GET /api/tags                    - 전체 Tag 요약 목록
GET /api/tags/{tag_no}           - Tag 상세
GET /api/tags/{tag_no}/documents - Tag 연관 문서/도면 목록
"""
from typing import List

from fastapi import APIRouter

from app.core.exceptions import ResourceNotFoundError
from app.models.schemas import (
    DocumentSummary,
    ErrorResponse,
    TagDetail,
    TagSummary,
)
from app.repositories.tag_repository import findAllTags
from app.services.tag_service import getDocumentsForTag, getTagDetail

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get(
    "",
    response_model=List[TagSummary],
    summary="전체 Tag 요약 목록",
    responses={503: {"model": ErrorResponse}},
)
def listTagsRoute() -> List[TagSummary]:
    return findAllTags()


@router.get(
    "/{tagNo}",
    response_model=TagDetail,
    summary="Tag 상세 (모든 부가 속성 포함)",
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def getTagDetailRoute(tagNo: str) -> TagDetail:
    detail = getTagDetail(tagNo)
    if detail is None:
        raise ResourceNotFoundError(
            f"Tag '{tagNo}' not found",
            code="TAG_NOT_FOUND",
        )
    return detail


@router.get(
    "/{tagNo}/documents",
    response_model=List[DocumentSummary],
    summary="Tag 와 연관된 문서/도면 목록",
    responses={503: {"model": ErrorResponse}},
)
def getTagDocumentsRoute(tagNo: str) -> List[DocumentSummary]:
    return getDocumentsForTag(tagNo)
