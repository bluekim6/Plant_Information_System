"""
헬스체크 라우터.

GET /api/health  - 서버 상태 + 엑셀 로딩 상태

엑셀 로딩에 한 건이라도 실패가 있으면 status="degraded" 로 응답하되
HTTP 자체는 200 으로 반환한다 (모니터링 도구 친화적).
"""
from typing import List

from fastapi import APIRouter

from app.core.config import getSettings
from app.data.excel_loader import preloadAll
from app.models.schemas import DataStatus, HealthStatus

router = APIRouter(prefix="/api", tags=["health"])


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="서버 + 엑셀 로딩 상태",
)
def healthRoute() -> HealthStatus:
    """서버가 살아 있고 엑셀이 적재되어 있는지 확인."""
    settings = getSettings()
    errors: List[str] = []
    rowCounts = preloadAll(onError=lambda msg: errors.append(msg))

    return HealthStatus(
        status="ok" if not errors else "degraded",
        appName=settings.appName,
        appVersion=settings.appVersion,
        data=DataStatus(rowCounts=rowCounts, errors=errors),
    )
