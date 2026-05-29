"""
Document 서비스.

문서 상세 + 문서가 가지는 Tag 목록 (PRD 시나리오 D).
"""
from typing import List, Optional

from app.models.schemas import DocumentDetail, TagSummary
from app.repositories.document_repository import (
    findDocumentByNo,
    findTagsByDocument,
)
from app.repositories.tag_repository import findTagByNo


def getDocumentDetail(documentNo: str) -> Optional[DocumentDetail]:
    """문서 상세 정보."""
    return findDocumentByNo(documentNo)


def getTagsForDocument(documentNo: str) -> List[TagSummary]:
    """문서가 포함하는 Tag 목록.

    Document_to_Tag 로 tagNo 만 얻은 뒤,
    Tag_Register 와 조인하여 description/system/package 를 채운다.
    Tag_Register 에 없는 tagNo 는 tagNo 만 있는 요약으로 반환.
    """
    tagNos = findTagsByDocument(documentNo)
    if not tagNos:
        return []

    summaries: List[TagSummary] = []
    for tagNo in tagNos:
        detail = findTagByNo(tagNo)
        if detail is None:
            summaries.append(TagSummary(tagNo=tagNo))
        else:
            summaries.append(
                TagSummary(
                    tagNo=detail.tagNo,
                    description=detail.description,
                    systemName=detail.systemName,
                    packageName=detail.packageName,
                    manufactureName=detail.manufactureName,
                )
            )
    return summaries
