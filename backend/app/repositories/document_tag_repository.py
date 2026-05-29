"""
Document-Tag 관계 접근 레이어 (호환용).

실제 N:M 매핑은 document_repository 에서 일괄 처리한다.
이 모듈은 'Tag로 docNo 만' 또는 'Document로 tagNo 만' 빠르게 얻고 싶을 때
사용하는 가벼운 진입점이다.
"""
from typing import List

from app.repositories.document_repository import (
    findDocumentNosByTag,
    findTagsByDocument,
)

__all__ = ["findDocumentsByTag", "findTagsByDocument"]


def findDocumentsByTag(tagNo: str) -> List[str]:
    """Tag 에 연결된 문서번호 목록."""
    return findDocumentNosByTag(tagNo)
