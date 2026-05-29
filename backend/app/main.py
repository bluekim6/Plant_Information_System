"""
FastAPI 애플리케이션 엔트리포인트.

각 라우터는 app/api/routes 하위 모듈에 정의되어 있으며,
이 파일에서는 앱 인스턴스 생성, 미들웨어, lifespan, 에러 핸들러 등록만 담당한다.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handlers import registerErrorHandlers
from app.api.routes import (
    comments as commentsRoute,
    diagnostics as diagnosticsRoute,
    documents as documentsRoute,
    drawings as drawingsRoute,
    health as healthRoute,
    hierarchy as hierarchyRoute,
    history as historyRoute,
    manufactures as manufacturesRoute,
    packages as packagesRoute,
    search as searchRoute,
    systems as systemsRoute,
    tags as tagsRoute,
)
from app.core.config import getSettings
from app.data.excel_loader import preloadAll

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """앱 시작 시 엑셀 사전 로딩 (검증)."""
    errors = []
    rowCounts = preloadAll(onError=lambda msg: errors.append(msg))

    logger.info("Excel preload row counts: %s", rowCounts)
    if errors:
        for e in errors:
            logger.error("Excel preload error: %s", e)

    yield


def createApp() -> FastAPI:
    """FastAPI 앱 객체를 생성하고 라우터/미들웨어/에러 핸들러를 등록한다."""
    settings = getSettings()

    app = FastAPI(
        title=settings.appName,
        version=settings.appVersion,
        lifespan=lifespan,
    )

    # 로컬 개발 환경에서 React dev server 와의 통신을 위한 CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.corsOrigins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 통일 에러 응답 형식 등록
    registerErrorHandlers(app)

    # 도메인별 라우터 등록 (prefix 는 각 라우터 모듈 내부에서 정의)
    app.include_router(healthRoute.router)
    app.include_router(systemsRoute.router)
    app.include_router(packagesRoute.router)
    app.include_router(tagsRoute.router)
    app.include_router(documentsRoute.router)
    app.include_router(drawingsRoute.router)
    app.include_router(manufacturesRoute.router)
    app.include_router(searchRoute.router)
    app.include_router(commentsRoute.router)
    app.include_router(historyRoute.router)
    app.include_router(diagnosticsRoute.router)

    # 후방 호환: 이전 단계에서 사용된 /api/hierarchy/* 경로 유지
    app.include_router(hierarchyRoute.router)

    return app


app = createApp()
