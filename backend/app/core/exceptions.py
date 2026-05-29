"""
도메인 예외 정의.

라우터/서비스에서 HTTPException 을 직접 던지지 않고 이 예외들을 사용하면,
api/error_handlers.py 의 핸들러가 통일된 에러 응답으로 변환한다.
"""
from typing import Optional


class AppError(Exception):
    """애플리케이션 도메인 예외의 기본 클래스."""

    statusCode: int = 500
    code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        statusCode: Optional[int] = None,
    ) -> None:
        self.message = message
        if code is not None:
            self.code = code
        if statusCode is not None:
            self.statusCode = statusCode
        super().__init__(message)


class ResourceNotFoundError(AppError):
    """요청 자원이 존재하지 않을 때 사용 (HTTP 404)."""

    statusCode = 404
    code = "NOT_FOUND"


class InvalidQueryError(AppError):
    """쿼리 파라미터가 잘못되었을 때 사용 (HTTP 400)."""

    statusCode = 400
    code = "INVALID_QUERY"
