"""
Tag 데이터 접근 레이어.

Tag_Register.xlsx 의 DataFrame 을 도메인 객체로 변환하여 반환한다.
DataFrame 자체는 외부에 노출하지 않는다.
"""
from typing import Dict, List, Optional

import pandas as pd

from app.core.column_map import TagColumns
from app.data.excel_loader import loadTagRegister
from app.models.schemas import TagDetail, TagSummary


def _toSummary(row: pd.Series) -> TagSummary:
    return TagSummary(
        tagNo=row[TagColumns.TAG],
        description=row.get(TagColumns.DESCRIPTION) or None,
        systemName=row.get(TagColumns.SYSTEM) or None,
        packageName=row.get(TagColumns.PACKAGE) or None,
        manufactureName=row.get(TagColumns.MANUFACTURE_NAME) or None,
    )


_CORE_TAG_COLUMNS = set(TagColumns.CORE)


def _toDetail(row: pd.Series) -> TagDetail:
    # 핵심 컬럼을 제외한 나머지 컬럼을 동적 속성으로 모아 보존
    # (EQUIPMENT CLASS, VENDOR, MODEL DESCRIPTION, P&ID NUMBER 등)
    attributes: Dict[str, str] = {
        col: row[col]
        for col in row.index
        if str(col) not in _CORE_TAG_COLUMNS
    }
    return TagDetail(
        tagNo=row[TagColumns.TAG],
        description=row.get(TagColumns.DESCRIPTION) or None,
        systemName=row.get(TagColumns.SYSTEM) or None,
        packageName=row.get(TagColumns.PACKAGE) or None,
        manufactureName=row.get(TagColumns.MANUFACTURE_NAME) or None,
        referenceDrawing=row.get(TagColumns.REFERENCE_DRAWING) or None,
        attributes=attributes,
    )


def findAllTags() -> List[TagSummary]:
    """전체 Tag 목록 반환."""
    df = loadTagRegister()
    return [_toSummary(row) for _, row in df.iterrows()]


def findTagByNo(tagNo: str) -> Optional[TagDetail]:
    """Tag No 로 단일 Tag 상세 조회. 없으면 None."""
    df = loadTagRegister()
    matched = df[df[TagColumns.TAG] == tagNo]
    if matched.empty:
        return None
    return _toDetail(matched.iloc[0])


def findTagsByPackage(packageName: str) -> List[TagSummary]:
    """Package 에 속한 Tag 목록 반환."""
    df = loadTagRegister()
    matched = df[df[TagColumns.PACKAGE] == packageName]
    return [_toSummary(row) for _, row in matched.iterrows()]


def findTagsBySystem(systemName: str) -> List[TagSummary]:
    """System 에 속한 Tag 목록 반환 (계층 통계용)."""
    df = loadTagRegister()
    matched = df[df[TagColumns.SYSTEM] == systemName]
    return [_toSummary(row) for _, row in matched.iterrows()]


def listSystemNames() -> List[str]:
    """전체 System 이름 목록 (중복 제거, 알파벳 순)."""
    df = loadTagRegister()
    return sorted({s for s in df[TagColumns.SYSTEM] if s})


def listPackageNames(systemName: Optional[str] = None) -> List[str]:
    """전체 또는 특정 System 의 Package 이름 목록."""
    df = loadTagRegister()
    if systemName is not None:
        df = df[df[TagColumns.SYSTEM] == systemName]
    return sorted({p for p in df[TagColumns.PACKAGE] if p})
