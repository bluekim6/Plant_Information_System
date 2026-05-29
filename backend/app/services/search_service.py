"""
통합 검색 서비스 (PRD 9.2).

Tag No, Description, System, Package, 문서번호, 도면번호 컬럼에서
부분 일치(대소문자 무시)로 검색한다.
"""
from typing import List

import pandas as pd

from app.core.column_map import DocumentColumns, TagColumns
from app.data.excel_loader import loadDocumentList, loadTagRegister
from app.models.schemas import SearchHit


def searchAll(query: str, limit: int = 50) -> List[SearchHit]:
    """전체 데이터에서 query 와 일치하는 항목을 반환한다."""
    q = (query or "").strip().lower()
    if not q:
        return []

    hits: List[SearchHit] = []

    tagDf = loadTagRegister()
    tagMask = (
        tagDf[TagColumns.TAG].str.lower().str.contains(q, na=False)
        | tagDf[TagColumns.DESCRIPTION].str.lower().str.contains(q, na=False)
    )
    for _, row in tagDf[tagMask].head(limit).iterrows():
        hits.append(
            SearchHit(
                hitType="tag",
                key=row[TagColumns.TAG],
                label=f"{row[TagColumns.TAG]} - {row[TagColumns.DESCRIPTION]}",
            )
        )

    seenSystems = set()
    for s in tagDf.loc[
        tagDf[TagColumns.SYSTEM].str.lower().str.contains(q, na=False),
        TagColumns.SYSTEM,
    ]:
        if s and s not in seenSystems:
            seenSystems.add(s)
            hits.append(SearchHit(hitType="system", key=s, label=s))

    seenPackages = set()
    for p in tagDf.loc[
        tagDf[TagColumns.PACKAGE].str.lower().str.contains(q, na=False),
        TagColumns.PACKAGE,
    ]:
        if p and p not in seenPackages:
            seenPackages.add(p)
            hits.append(SearchHit(hitType="package", key=p, label=p))

    docDf: pd.DataFrame = loadDocumentList()
    docMask = (
        docDf[DocumentColumns.DOCUMENT_NUMBER].str.lower().str.contains(q, na=False)
        | docDf[DocumentColumns.DOCUMENT_NAME].str.lower().str.contains(q, na=False)
    )
    for _, row in docDf[docMask].head(limit).iterrows():
        hits.append(
            SearchHit(
                hitType="document",
                key=row[DocumentColumns.DOCUMENT_NUMBER],
                label=f"{row[DocumentColumns.DOCUMENT_NUMBER]} - {row[DocumentColumns.DOCUMENT_NAME]}",
            )
        )

    return hits[:limit]
