"""
History (변경 이력) 데이터 접근 레이어.

쓰기는 append 만 허용한다 (감사 로그 성격).
"""
from typing import List

from app.core.config import getSettings
from app.data.json_store import newLock, readJson, writeJsonAtomic
from app.models.history_schema import HistoryEntry

_lock = newLock()


def _readAll() -> List[dict]:
    return readJson(getSettings().historyPath)


def _writeAll(items: List[dict]) -> None:
    writeJsonAtomic(getSettings().historyPath, items)


def append(entry: HistoryEntry) -> HistoryEntry:
    """이력 1건 추가."""
    payload = entry.model_dump(mode="json")
    with _lock:
        items = _readAll()
        items.append(payload)
        _writeAll(items)
    return entry


def listAll() -> List[HistoryEntry]:
    with _lock:
        items = _readAll()
    return [HistoryEntry(**i) for i in items]


def listByCommentId(commentId: str) -> List[HistoryEntry]:
    return [h for h in listAll() if h.commentId == commentId]


def listByTag(tagNo: str) -> List[HistoryEntry]:
    return [h for h in listAll() if h.tagNo == tagNo]
