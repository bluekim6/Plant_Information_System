"""
Document 데이터 접근 레이어.

Document_List.xlsx + Document_to_Tag.xlsx 를 조합하여
- 문서 단건 조회
- 문서 전체 목록
- Tag 기준 관련 문서 찾기
- Document 기준 관련 Tag 찾기
를 제공한다.
"""
from pathlib import Path
from typing import List, Optional

import pandas as pd

from app.core.column_map import DocumentColumns, DocumentToTagColumns
from app.core.config import getSettings
from app.data.excel_loader import loadDocumentList, loadDocumentToTag
from app.models.schemas import DocumentDetail, DocumentSummary


def _toSummary(row: pd.Series) -> DocumentSummary:
    return DocumentSummary(
        documentNo=row[DocumentColumns.DOCUMENT_NUMBER],
        documentName=row.get(DocumentColumns.DOCUMENT_NAME) or None,
        revision=row.get(DocumentColumns.REVISION) or None,
    )


def _resolvePdfPath(documentNo: str) -> Optional[Path]:
    """문서번호 -> PDF 절대경로 매핑. 파일명 규칙: '{documentNo}.pdf'."""
    if not documentNo:
        return None
    settings = getSettings()
    candidate = settings.drawingStoragePath / f"{documentNo}.pdf"
    return candidate if candidate.exists() else None


def findAllDocuments() -> List[DocumentSummary]:
    """전체 문서 목록 반환."""
    df = loadDocumentList()
    return [_toSummary(row) for _, row in df.iterrows()]


def findDocumentByNo(documentNo: str) -> Optional[DocumentDetail]:
    """문서번호로 단건 조회."""
    df = loadDocumentList()
    matched = df[df[DocumentColumns.DOCUMENT_NUMBER] == documentNo]
    if matched.empty:
        return None
    row = matched.iloc[0]
    return DocumentDetail(
        documentNo=row[DocumentColumns.DOCUMENT_NUMBER],
        documentName=row.get(DocumentColumns.DOCUMENT_NAME) or None,
        revision=row.get(DocumentColumns.REVISION) or None,
        pdfAvailable=_resolvePdfPath(row[DocumentColumns.DOCUMENT_NUMBER]) is not None,
    )


def findDocumentNosByTag(tagNo: str) -> List[str]:
    """Tag 와 연결된 문서번호 목록."""
    link = loadDocumentToTag()
    return [
        d
        for d in link.loc[
            link[DocumentToTagColumns.TAG] == tagNo,
            DocumentToTagColumns.DOCUMENT_NUMBER,
        ].tolist()
        if d
    ]


def findDocumentsByTag(tagNo: str) -> List[DocumentSummary]:
    """Tag 와 연결된 문서 요약 목록.

    Document_to_Tag 로 documentNo 를 얻은 뒤,
    Document_List 와 조인하여 이름/리비전을 채운다.
    """
    docNos = findDocumentNosByTag(tagNo)
    if not docNos:
        return []

    df = loadDocumentList()
    docs = df[df[DocumentColumns.DOCUMENT_NUMBER].isin(docNos)]

    # 매핑은 있으나 Document_List 에 없는 문서번호도 포함하여 반환
    found: List[DocumentSummary] = [_toSummary(row) for _, row in docs.iterrows()]
    knownNos = {d.documentNo for d in found}
    for n in docNos:
        if n not in knownNos:
            found.append(DocumentSummary(documentNo=n))
    return found


def findTagsByDocument(documentNo: str) -> List[str]:
    """문서가 포함하는 Tag 번호 목록 (PRD 시나리오 D)."""
    link = loadDocumentToTag()
    return [
        t
        for t in link.loc[
            link[DocumentToTagColumns.DOCUMENT_NUMBER] == documentNo,
            DocumentToTagColumns.TAG,
        ].tolist()
        if t
    ]
