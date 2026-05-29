"""
계층 구조 서비스 (System -> Package -> Tag).

Tag_Register 의 distinct 값을 이용하여 계층을 만든다.
"""
from typing import List

import pandas as pd

from app.core.column_map import TagColumns
from app.data.excel_loader import loadTagRegister
from app.models.schemas import PackageNode, SystemNode, TagSummary
from app.repositories.tag_repository import findTagsByPackage


def listSystems() -> List[SystemNode]:
    """전체 System 목록 + 각 System 이 가진 Package 수."""
    df = loadTagRegister()
    grouped: pd.DataFrame = (
        df[[TagColumns.SYSTEM, TagColumns.PACKAGE]]
        .replace("", pd.NA)
        .dropna(subset=[TagColumns.SYSTEM])
        .groupby(TagColumns.SYSTEM)[TagColumns.PACKAGE]
        .nunique()
        .reset_index(name="packageCount")
        .sort_values(TagColumns.SYSTEM)
    )
    return [
        SystemNode(systemName=row[TagColumns.SYSTEM], packageCount=int(row["packageCount"]))
        for _, row in grouped.iterrows()
    ]


def listPackagesBySystem(systemName: str) -> List[PackageNode]:
    """특정 System 에 속한 Package 목록 + 각 Package 의 Tag 수."""
    df = loadTagRegister()
    sub = df[df[TagColumns.SYSTEM] == systemName]
    if sub.empty:
        return []
    grouped = (
        sub.replace("", pd.NA)
        .dropna(subset=[TagColumns.PACKAGE])
        .groupby(TagColumns.PACKAGE)[TagColumns.TAG]
        .count()
        .reset_index(name="tagCount")
        .sort_values(TagColumns.PACKAGE)
    )
    return [
        PackageNode(
            packageName=row[TagColumns.PACKAGE],
            systemName=systemName,
            tagCount=int(row["tagCount"]),
        )
        for _, row in grouped.iterrows()
    ]


def listTagsByPackage(packageName: str) -> List[TagSummary]:
    """특정 Package 에 속한 Tag 목록."""
    return findTagsByPackage(packageName)
