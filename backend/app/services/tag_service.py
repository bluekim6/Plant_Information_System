"""
Tag 서비스.

Tag 상세 정보 + Tag 와 연결된 문서 목록 조회.
"""
from typing import List, Optional

from app.models.schemas import DocumentSummary, TagDetail
from app.repositories.document_repository import findDocumentsByTag
from app.repositories.tag_repository import findTagByNo


def getTagDetail(tagNo: str) -> Optional[TagDetail]:
    """Tag 상세 정보를 반환한다."""
    return findTagByNo(tagNo)


def getDocumentsForTag(tagNo: str) -> List[DocumentSummary]:
    """Tag 에 연결된 문서/도면 목록을 반환한다."""
    return findDocumentsByTag(tagNo)
