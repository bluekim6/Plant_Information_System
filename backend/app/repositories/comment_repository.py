"""
Comment 데이터 접근 레이어.

저장 형식: JSON 배열 (한 파일에 모든 Tag 의 Comment).
이 모듈만 교체하면 SQLite/PostgreSQL 등으로 자유롭게 갈아탈 수 있다.
"""
from typing import List, Optional

from app.core.config import getSettings
from app.data.json_store import newLock, readJson, writeJsonAtomic
from app.models.comment_schema import Comment

_lock = newLock()


def _readAll() -> List[dict]:
    return readJson(getSettings().commentsPath)


def _writeAll(items: List[dict]) -> None:
    writeJsonAtomic(getSettings().commentsPath, items)


def listAll() -> List[Comment]:
    """모든 Comment."""
    with _lock:
        items = _readAll()
    return [Comment(**i) for i in items]


def listByTag(tagNo: str) -> List[Comment]:
    """특정 Tag 의 Comment 만 반환."""
    return [c for c in listAll() if c.tagNo == tagNo]


def findById(commentId: str) -> Optional[Comment]:
    """단건 조회. 없으면 None."""
    return next((c for c in listAll() if c.id == commentId), None)


def save(comment: Comment) -> Comment:
    """존재하면 update, 없으면 insert (upsert)."""
    payload = comment.model_dump(mode="json")
    with _lock:
        items = _readAll()
        idx = next(
            (i for i, x in enumerate(items) if x.get("id") == comment.id),
            None,
        )
        if idx is None:
            items.append(payload)
        else:
            items[idx] = payload
        _writeAll(items)
    return comment


def delete(commentId: str) -> bool:
    """삭제. 대상 존재 시 True."""
    with _lock:
        items = _readAll()
        remaining = [x for x in items if x.get("id") != commentId]
        if len(remaining) == len(items):
            return False
        _writeAll(remaining)
    return True
