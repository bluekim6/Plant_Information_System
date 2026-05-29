"""
Document 라우터.

GET /api/documents                       - 전체 문서 목록
GET /api/documents/{document_no}         - 문서 상세
GET /api/documents/{document_no}/tags    - 도면이 가진 Tag 목록 (시나리오 D)
"""
from typing import List

from fastapi import APIRouter

from app.core.exceptions import ResourceNotFoundError
from app.models.schemas import (
    DocumentDetail,
    DocumentSummary,
    ErrorResponse,
    TagSummary,
)
from app.repositories.document_repository import findAllDocuments
from app.services.document_service import getDocumentDetail, getTagsForDocument

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get(
    "",
    response_model=List[DocumentSummary],
    summary="전체 문서/도면 목록",
    responses={503: {"model": ErrorResponse}},
)
def listDocumentsRoute() -> List[DocumentSummary]:
    return findAllDocuments()


@router.get(
    "/{documentNo}",
    response_model=DocumentDetail,
    summary="문서 상세 (PDF 존재 여부 포함)",
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def getDocumentDetailRoute(documentNo: str) -> DocumentDetail:
    detail = getDocumentDetail(documentNo)
    if detail is None:
        raise ResourceNotFoundError(
            f"Document '{documentNo}' not found",
            code="DOCUMENT_NOT_FOUND",
        )
    return detail


@router.get(
    "/{documentNo}/tags",
    response_model=List[TagSummary],
    summary="도면이 가진 Tag 목록",
    responses={503: {"model": ErrorResponse}},
)
def getDocumentTagsRoute(documentNo: str) -> List[TagSummary]:
    return getTagsForDocument(documentNo)
