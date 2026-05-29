"""
도면(PDF) 라우터.

GET /api/drawings/{document_no}            - 인라인 표시 (iframe / 새 창 미리보기)
GET /api/drawings/{document_no}/download   - 첨부 다운로드

두 엔드포인트는 같은 파일을 응답하지만 Content-Disposition 헤더만 다르다.
- inline   : 브라우저가 자체 PDF 뷰어로 표시 (iframe 임베드 가능)
- attachment: 브라우저가 파일로 저장
"""
from fastapi import APIRouter

from app.core.exceptions import ResourceNotFoundError
from app.models.schemas import ErrorResponse
from app.services.drawing_service import resolveDrawingPath
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/drawings", tags=["drawings"])


def _pdfResponse(documentNo: str, dispositionType: str) -> FileResponse:
    pdfPath = resolveDrawingPath(documentNo)
    if pdfPath is None:
        raise ResourceNotFoundError(
            f"Drawing '{documentNo}' not found",
            code="DRAWING_NOT_FOUND",
        )
    return FileResponse(
        path=str(pdfPath),
        media_type="application/pdf",
        filename=pdfPath.name,
        content_disposition_type=dispositionType,
    )


@router.get(
    "/{documentNo}",
    summary="도면 PDF 인라인 (iframe / 새 창 미리보기)",
    responses={404: {"model": ErrorResponse}},
)
def getDrawingInlineRoute(documentNo: str) -> FileResponse:
    """도면 PDF 를 inline 으로 응답한다."""
    return _pdfResponse(documentNo, "inline")


@router.get(
    "/{documentNo}/download",
    summary="도면 PDF 다운로드 (첨부)",
    responses={404: {"model": ErrorResponse}},
)
def getDrawingDownloadRoute(documentNo: str) -> FileResponse:
    """도면 PDF 를 attachment 로 응답하여 브라우저가 저장하도록 한다."""
    return _pdfResponse(documentNo, "attachment")
