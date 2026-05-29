"""
통합 검색 라우터.

GET /api/search?q=...&limit=...

Tag No, Tag Description, System, Package, Document Number, Document Name
컬럼에서 부분 일치(대소문자 무시)로 검색한다.
"""
from typing import List

from fastapi import APIRouter

from app.core.exceptions import InvalidQueryError
from app.models.schemas import ErrorResponse, SearchHit
from app.services.search_service import searchAll

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get(
    "",
    response_model=List[SearchHit],
    summary="Tag/System/Package/Document 통합 검색",
    responses={
        400: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def searchRoute(q: str = "", limit: int = 50) -> List[SearchHit]:
    if not q.strip():
        raise InvalidQueryError(
            "query parameter 'q' must not be empty",
            code="EMPTY_QUERY",
        )
    if limit < 1 or limit > 500:
        raise InvalidQueryError(
            "limit must be between 1 and 500",
            code="INVALID_LIMIT",
        )
    return searchAll(q, limit=limit)
