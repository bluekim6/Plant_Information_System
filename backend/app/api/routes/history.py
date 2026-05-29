"""
변경 이력 라우터.

GET /api/tags/{tagNo}/history          - Tag 단위 변경 이력 (최신순)
GET /api/comments/{commentId}/history  - Comment 단위 변경 이력 (최신순)
"""
from typing import List

from fastapi import APIRouter

from app.models.history_schema import HistoryEntry
from app.services import history_service

router = APIRouter(tags=["history"])


@router.get(
    "/api/tags/{tagNo}/history",
    response_model=List[HistoryEntry],
    summary="Tag 단위 변경 이력",
)
def listTagHistoryRoute(tagNo: str) -> List[HistoryEntry]:
    return history_service.listHistoryByTag(tagNo)


@router.get(
    "/api/comments/{commentId}/history",
    response_model=List[HistoryEntry],
    summary="Comment 단위 변경 이력",
)
def listCommentHistoryRoute(commentId: str) -> List[HistoryEntry]:
    return history_service.listHistoryByCommentId(commentId)
