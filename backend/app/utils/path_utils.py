"""
경로 관련 유틸리티.

PDF 파일명 정규화, 안전한 경로 결합 등 공용 헬퍼.
"""
from pathlib import Path


def safeJoin(baseDir: Path, relative: str) -> Path:
    """baseDir 바깥으로 빠져나가는 경로를 차단하며 결합한다.

    경로 탐색 공격(../) 방지용.
    """
    candidate = (baseDir / relative).resolve()
    base = baseDir.resolve()
    if not candidate.is_relative_to(base):
        raise ValueError(f"허용되지 않은 경로: {relative}")
    return candidate
