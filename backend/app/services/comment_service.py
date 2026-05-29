"""
Comment 서비스.

CRUD 와 상태 변경을 담당하고, 모든 변경에 대해 history_service 로
이력을 자동 기록한다.
"""
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from app.core.exceptions import ResourceNotFoundError
from app.models.comment_schema import (
    Comment,
    CommentCreate,
    CommentStatusChange,
    CommentUpdate,
)
from app.repositories import comment_repository
from app.services import history_service


def listByTag(tagNo: str) -> List[Comment]:
    """Tag 의 Comment 목록을 작성 시간 순(오래된 → 최신)으로 반환."""
    items = comment_repository.listByTag(tagNo)
    return sorted(items, key=lambda c: c.createdAt)


def get(commentId: str) -> Comment:
    """단건 조회. 없으면 ResourceNotFoundError."""
    c = comment_repository.findById(commentId)
    if c is None:
        raise ResourceNotFoundError(
            f"Comment '{commentId}' not found",
            code="COMMENT_NOT_FOUND",
        )
    return c


def create(tagNo: str, body: CommentCreate) -> Comment:
    """Comment 생성 + history.created 기록."""
    now = datetime.now(timezone.utc)
    comment = Comment(
        id=str(uuid4()),
        tagNo=tagNo,
        content=body.content,
        author=body.author,
        status="Open",
        linkedDocumentNo=body.linkedDocumentNo,
        createdAt=now,
        updatedAt=now,
    )
    saved = comment_repository.save(comment)
    history_service.recordCommentEvent(
        commentId=saved.id,
        tagNo=saved.tagNo,
        action="created",
        author=saved.author,
        after=saved.model_dump(mode="json"),
    )
    return saved


def update(commentId: str, body: CommentUpdate) -> Comment:
    """Comment 본문/연결 문서 수정 + history.updated 기록."""
    existing = get(commentId)
    before = existing.model_dump(mode="json")

    fields = existing.model_dump()
    if body.content is not None:
        fields["content"] = body.content
    if body.linkedDocumentNo is not None:
        fields["linkedDocumentNo"] = body.linkedDocumentNo
    fields["updatedAt"] = datetime.now(timezone.utc)
    updated = Comment(**fields)
    saved = comment_repository.save(updated)

    history_service.recordCommentEvent(
        commentId=saved.id,
        tagNo=saved.tagNo,
        action="updated",
        author=body.author,
        before=before,
        after=saved.model_dump(mode="json"),
    )
    return saved


def changeStatus(commentId: str, body: CommentStatusChange) -> Comment:
    """Comment 상태 전이 + history.status_changed 기록.

    같은 상태로의 전이는 무시(이력 없음).
    """
    existing = get(commentId)
    if existing.status == body.status:
        return existing

    fields = existing.model_dump()
    fields["status"] = body.status
    fields["updatedAt"] = datetime.now(timezone.utc)
    updated = Comment(**fields)
    saved = comment_repository.save(updated)

    history_service.recordCommentEvent(
        commentId=saved.id,
        tagNo=saved.tagNo,
        action="status_changed",
        author=body.author,
        before={"status": existing.status},
        after={"status": saved.status},
    )
    return saved


def delete(commentId: str, author: str) -> None:
    """Comment 삭제 + history.deleted 기록."""
    existing = get(commentId)
    before = existing.model_dump(mode="json")
    if not comment_repository.delete(commentId):
        raise ResourceNotFoundError(
            f"Comment '{commentId}' not found",
            code="COMMENT_NOT_FOUND",
        )
    history_service.recordCommentEvent(
        commentId=existing.id,
        tagNo=existing.tagNo,
        action="deleted",
        author=author or "unknown",
        before=before,
    )
