"""
진단 라우터.

엑셀 적재 상태 확인 및 강제 재로딩용.

GET  /api/diagnostics/data    - 4개 엑셀의 행 수와 에러 메시지
POST /api/diagnostics/reload  - 캐시 비우고 재로드
"""
from typing import List

from fastapi import APIRouter

from app.data.excel_loader import preloadAll, reloadAll
from app.models.schemas import DataStatus

router = APIRouter(prefix="/api/diagnostics", tags=["diagnostics"])


@router.get("/data", response_model=DataStatus)
def getDataStatusRoute():
    """엑셀 적재 상태를 반환한다 (에러가 있어도 응답은 성공)."""
    errors: List[str] = []
    rowCounts = preloadAll(onError=lambda msg: errors.append(msg))
    return DataStatus(rowCounts=rowCounts, errors=errors)


@router.post("/reload", response_model=DataStatus)
def reloadDataRoute():
    """엑셀 캐시를 비우고 재로드한다."""
    reloadAll()
    errors: List[str] = []
    rowCounts = preloadAll(onError=lambda msg: errors.append(msg))
    return DataStatus(rowCounts=rowCounts, errors=errors)
