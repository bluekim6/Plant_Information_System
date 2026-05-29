"""
간단한 JSON 파일 저장소 헬퍼.

Comment / History repository 가 공유하는 atomic write + read 유틸.
DB 로 교체할 때는 이 파일을 수정하지 않고 repository 가 다른 backend 를
사용하도록만 바꾸면 된다.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import List


def readJson(path: Path) -> List[dict]:
    """파일이 없으면 빈 리스트 반환, 있으면 list[dict] 로드."""
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def writeJsonAtomic(path: Path, items: List[dict]) -> None:
    """동일 파티션 임시파일에 쓴 뒤 os.replace 로 원자적 교체."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False, default=str)
    os.replace(tmp, path)


def newLock() -> Lock:
    """저장소별 lock 인스턴스를 만든다 (단순 반환 헬퍼)."""
    return Lock()
