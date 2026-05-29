"""
엑셀 로더.

4개 엑셀 파일을 메모리에 적재하고, mtime 기반으로 변경 시 자동 재로드한다.
파일 단위로 함수를 분리하여, 한 파일이 변해도 다른 파일은 다시 읽지 않는다.

주요 기능:
- loadTagRegister()      -> Tag_Register DataFrame
- loadDocumentList()     -> Document_List DataFrame
- loadDocumentToTag()    -> Document_to_Tag DataFrame
- loadManufactureList()  -> Manufacture_list DataFrame
- reloadAll()            -> 캐시 비우고 강제 재로드
- preloadAll()           -> 시작 시 모든 엑셀 미리 로드 (검증 목적)
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Callable, Dict, List, Optional

import pandas as pd

from app.core.column_map import (
    DocumentColumns,
    DocumentToTagColumns,
    ManufactureColumns,
    TagColumns,
)
from app.core.config import getSettings
from app.data.validators import (
    ExcelDataError,
    validateFileExists,
    validateRequiredColumns,
)


@dataclass
class _CacheEntry:
    """엑셀 한 파일의 캐시 엔트리."""

    df: pd.DataFrame
    mtime: float


_cache: Dict[str, _CacheEntry] = {}
_cacheLock = Lock()


def _readExcel(filePath: Path, label: str, requiredColumns: List[str]) -> pd.DataFrame:
    """엑셀을 읽고 검증한 뒤 DataFrame 을 반환한다.

    - dtype=str 로 통일하여 숫자/날짜 자동 변환을 막는다.
    - NaN 은 빈 문자열로 치환한다.
    - 모든 문자열 컬럼은 양쪽 공백을 제거한다.
    """
    validateFileExists(filePath, label)
    try:
        df = pd.read_excel(filePath, dtype=str).fillna("")
    except Exception as exc:
        raise ExcelDataError(
            f"[{label}] 엑셀 파일을 읽는 중 오류가 발생했습니다: {exc}"
        ) from exc

    df.columns = [str(c).strip() for c in df.columns]
    validateRequiredColumns(df, requiredColumns, label)

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def _loadWithCache(
    cacheKey: str,
    filePath: Path,
    label: str,
    requiredColumns: List[str],
) -> pd.DataFrame:
    """파일 mtime 비교로 캐시를 갱신하며 DataFrame 을 반환한다."""
    validateFileExists(filePath, label)
    currentMtime = filePath.stat().st_mtime

    with _cacheLock:
        entry = _cache.get(cacheKey)
        if entry is not None and entry.mtime == currentMtime:
            return entry.df

        df = _readExcel(filePath, label, requiredColumns)
        _cache[cacheKey] = _CacheEntry(df=df, mtime=currentMtime)
        return df


def loadTagRegister() -> pd.DataFrame:
    """Tag_Register.xlsx 를 DataFrame 으로 반환."""
    settings = getSettings()
    return _loadWithCache(
        cacheKey="tag_register",
        filePath=settings.tagRegisterPath,
        label="Tag_Register",
        requiredColumns=TagColumns.REQUIRED,
    )


def loadDocumentList() -> pd.DataFrame:
    """Document_List.xlsx 를 DataFrame 으로 반환."""
    settings = getSettings()
    return _loadWithCache(
        cacheKey="document_list",
        filePath=settings.documentListPath,
        label="Document_List",
        requiredColumns=DocumentColumns.REQUIRED,
    )


def loadDocumentToTag() -> pd.DataFrame:
    """Document_to_Tag.xlsx 를 DataFrame 으로 반환."""
    settings = getSettings()
    return _loadWithCache(
        cacheKey="document_to_tag",
        filePath=settings.documentToTagPath,
        label="Document_to_Tag",
        requiredColumns=DocumentToTagColumns.REQUIRED,
    )


def loadManufactureList() -> pd.DataFrame:
    """Manufacture_list.xlsx 를 DataFrame 으로 반환."""
    settings = getSettings()
    return _loadWithCache(
        cacheKey="manufacture_list",
        filePath=settings.manufactureListPath,
        label="Manufacture_list",
        requiredColumns=ManufactureColumns.REQUIRED,
    )


def reloadAll() -> None:
    """캐시를 비워 다음 호출 시 모든 엑셀을 재로드하게 한다."""
    with _cacheLock:
        _cache.clear()


def preloadAll(onError: Optional[Callable[[str], None]] = None) -> Dict[str, int]:
    """4개 엑셀을 모두 로드하여 헤더/필수 컬럼 검증을 일괄 수행한다.

    Returns:
        파일별 행 수 dict. 예) {"tag_register": 499, ...}
    """
    loaders = [
        ("tag_register", loadTagRegister),
        ("document_list", loadDocumentList),
        ("document_to_tag", loadDocumentToTag),
        ("manufacture_list", loadManufactureList),
    ]
    rowCounts: Dict[str, int] = {}
    for key, loader in loaders:
        try:
            df = loader()
            rowCounts[key] = len(df)
        except ExcelDataError as exc:
            if onError is not None:
                onError(str(exc))
            else:
                raise
    return rowCounts
