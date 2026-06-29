"""
환경설정 모듈.

엑셀 파일 경로, PDF 도면 폴더 경로 등 외부 자원 경로를
.env 파일 또는 환경변수로부터 로드한다. 코드에 경로를 박지 않는다.
"""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/.env 의 절대경로. 작업 디렉토리(cwd)에 의존하지 않도록
# 이 파일 위치를 기준으로 계산한다.
# 파일 구조: backend/app/config/settings.py -> backend/.env
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
# 저장소 루트(엑셀/도면 파일이 위치하는 곳). PC 마다 절대경로가 달라지는 문제를
# 피하기 위해, .env 의 상대경로는 모두 이 루트를 기준으로 해석한다.
_REPO_ROOT = _BACKEND_DIR.parent
_ENV_FILE_PATH = _BACKEND_DIR / ".env"
_DEFAULT_DATA_DIR = _BACKEND_DIR / "data"


class Settings(BaseSettings):
    """애플리케이션 환경설정."""

    appName: str = "Plant Information System"
    appVersion: str = "0.1.0"

    # 엑셀 데이터 파일 경로. .env 에서 상대경로를 쓰면 저장소 루트 기준으로 해석된다.
    # .env 미지정 시에는 저장소 루트의 파일을 기본값으로 사용한다.
    tagRegisterPath: Path = Field(
        default=Path("Tag_Register.xlsx"), alias="TAG_REGISTER_PATH"
    )
    documentListPath: Path = Field(
        default=Path("Document_List.xlsx"), alias="DOCUMENT_LIST_PATH"
    )
    documentToTagPath: Path = Field(
        default=Path("Document_to_Tag.xlsx"), alias="DOCUMENT_TO_TAG_PATH"
    )
    manufactureListPath: Path = Field(
        default=Path("Manufacture_list.xlsx"), alias="MANUFACTURE_LIST_PATH"
    )

    # PDF 도면 저장 폴더
    drawingStoragePath: Path = Field(
        default=Path("Document_Storage"), alias="DRAWING_STORAGE_PATH"
    )

    # Comment / History JSON 저장 경로 (.env 미지정 시 backend/data/ 사용)
    commentsPath: Path = Field(
        default=_DEFAULT_DATA_DIR / "comments.json",
        alias="COMMENTS_PATH",
    )
    historyPath: Path = Field(
        default=_DEFAULT_DATA_DIR / "history.json",
        alias="HISTORY_PATH",
    )

    @field_validator(
        "tagRegisterPath",
        "documentListPath",
        "documentToTagPath",
        "manufactureListPath",
        "drawingStoragePath",
        "commentsPath",
        "historyPath",
        mode="after",
    )
    @classmethod
    def _resolveRelativeToRepoRoot(cls, value: Path) -> Path:
        """상대경로는 저장소 루트 기준으로, 절대경로는 그대로 사용한다."""
        return value if value.is_absolute() else (_REPO_ROOT / value)

    # CORS 허용 오리진 (프론트엔드 dev server)
    corsOrigins: List[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        alias="CORS_ORIGINS",
    )

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def getSettings() -> Settings:
    """설정 객체를 캐싱하여 반환한다."""
    return Settings()  # type: ignore[call-arg]
