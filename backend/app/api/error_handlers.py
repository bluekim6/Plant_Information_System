"""
통일 에러 응답 핸들러.

모든 에러 응답은 다음 형식을 따른다:

    {
      "error": {
        "code": "<UPPER_SNAKE_CODE>",
        "message": "사용자 친화적 메시지"
      }
    }

라우터는 HTTPException 대신 app.core.exceptions 의 도메인 예외를 던지면 된다.
FastAPI 가 던지는 RequestValidationError, HTTPException 도 같은 형식으로 매핑한다.
"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppError
from app.data.validators import ExcelDataError


def _wrap(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


def registerErrorHandlers(app: FastAPI) -> None:
    """앱에 에러 핸들러를 등록한다."""

    @app.exception_handler(AppError)
    async def appErrorHandler(_request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.statusCode,
            content=_wrap(exc.code, exc.message),
        )

    @app.exception_handler(ExcelDataError)
    async def excelErrorHandler(_request: Request, exc: ExcelDataError) -> JSONResponse:
        # 엑셀 파일/컬럼 문제는 서비스 미사용 가능 상태(503)로 처리
        return JSONResponse(
            status_code=503,
            content=_wrap("EXCEL_DATA_ERROR", str(exc)),
        )

    @app.exception_handler(StarletteHTTPException)
    async def httpErrorHandler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        # FastAPI 내부의 HTTPException 도 동일 형식으로 변환
        message = str(exc.detail) if exc.detail else "HTTP error"
        code = f"HTTP_{exc.status_code}"
        return JSONResponse(status_code=exc.status_code, content=_wrap(code, message))

    @app.exception_handler(RequestValidationError)
    async def validationErrorHandler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # 요청 파라미터/바디 검증 실패
        return JSONResponse(
            status_code=422,
            content=_wrap("REQUEST_VALIDATION_ERROR", str(exc.errors())),
        )
