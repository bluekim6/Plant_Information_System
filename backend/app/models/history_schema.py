"""
변경 이력(History) 도메인 스키마.

PRD 9.7:
  - 누가 / 언제 / 무엇을 변경했는지 추적.

현재는 Comment 변경 이력만 기록하지만, 추후 Tag/Document 변경 등으로
확장할 수 있도록 commentId 는 Optional 로 두고 tagNo / action 만 필수다.
"""
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel

HistoryAction = Literal["created", "updated", "status_changed", "deleted"]


class HistoryEntry(BaseModel):
    """변경 이력 1건."""

    id: str
    commentId: Optional[str] = None
    tagNo: str
    action: HistoryAction
    author: str
    timestamp: datetime
    before: Optional[Dict[str, Any]] = None
    after: Optional[Dict[str, Any]] = None
