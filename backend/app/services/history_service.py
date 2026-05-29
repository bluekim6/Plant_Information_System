"""
변경 이력 서비스.

이력 기록은 다른 service(특히 comment_service) 에서 호출하여 사용한다.
이력 조회는 라우트에서 직접 호출한다.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.models.history_schema import HistoryAction, HistoryEntry
from app.repositories import history_repository


def recordCommentEvent(
    commentId: Optional[str],
    tagNo: str,
    action: HistoryAction,
    author: str,
    before: Optional[Dict[str, Any]] = None,
    after: Optional[Dict[str, Any]] = None,
) -> HistoryEntry:
    """Comment 변경 이벤트를 기록한다."""
    entry = HistoryEntry(
        id=str(uuid4()),
        commentId=commentId,
        tagNo=tagNo,
        action=action,
        author=author,
        timestamp=datetime.now(timezone.utc),
        before=before,
        after=after,
    )
    return history_repository.append(entry)


def listHistoryByTag(tagNo: str) -> List[HistoryEntry]:
    """특정 Tag 의 변경 이력 (최신순)."""
    items = history_repository.listByTag(tagNo)
    return sorted(items, key=lambda x: x.timestamp, reverse=True)


def listHistoryByCommentId(commentId: str) -> List[HistoryEntry]:
    """특정 Comment 의 변경 이력 (최신순)."""
    items = history_repository.listByCommentId(commentId)
    return sorted(items, key=lambda x: x.timestamp, reverse=True)
