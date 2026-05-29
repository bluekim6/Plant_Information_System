"""
Comment 라우터.

GET    /api/tags/{tagNo}/comments         - Tag 의 Comment 목록
POST   /api/tags/{tagNo}/comments         - Comment 생성
PATCH  /api/comments/{commentId}          - Comment 본문/연결 문서 수정
PATCH  /api/comments/{commentId}/status   - 상태 전이 (Open/Review/Closed)
DELETE /api/comments/{commentId}          - Comment 삭제
"""
from typing import List

from fastapi import APIRouter, Query

from app.models.comment_schema import (
    Comment,
    CommentCreate,
    CommentStatusChange,
    CommentUpdate,
)
from app.models.schemas import ErrorResponse
from app.services import comment_service

router = APIRouter(tags=["comments"])


@router.get(
    "/api/tags/{tagNo}/comments",
    response_model=List[Comment],
    summary="Tag 의 Comment 목록 (오래된 순)",
)
def listCommentsRoute(tagNo: str) -> List[Comment]:
    return comment_service.listByTag(tagNo)


@router.post(
    "/api/tags/{tagNo}/comments",
    response_model=Comment,
    summary="Comment 생성",
)
def createCommentRoute(tagNo: str, body: CommentCreate) -> Comment:
    return comment_service.create(tagNo, body)


@router.patch(
    "/api/comments/{commentId}",
    response_model=Comment,
    summary="Comment 본문/연결 문서 수정",
    responses={404: {"model": ErrorResponse}},
)
def updateCommentRoute(commentId: str, body: CommentUpdate) -> Comment:
    return comment_service.update(commentId, body)


@router.patch(
    "/api/comments/{commentId}/status",
    response_model=Comment,
    summary="Comment 상태 변경 (Open / Review / Closed)",
    responses={404: {"model": ErrorResponse}},
)
def changeStatusRoute(commentId: str, body: CommentStatusChange) -> Comment:
    return comment_service.changeStatus(commentId, body)


@router.delete(
    "/api/comments/{commentId}",
    summary="Comment 삭제",
    responses={404: {"model": ErrorResponse}},
)
def deleteCommentRoute(
    commentId: str,
    author: str = Query("", description="삭제 수행자 이름 (이력 기록용)"),
) -> dict:
    comment_service.delete(commentId, author)
    return {"deleted": True}
