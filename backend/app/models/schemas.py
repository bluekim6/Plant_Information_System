"""
통합 Pydantic 스키마.

도메인별 응답 모델을 한 파일에 모아 관리한다.
필드명은 카멜케이스(camelCase) 를 사용하고, 엑셀 원본 컬럼명은
attributes dict 에 그대로 보존한다.
"""
from typing import Dict, List, Optional

from pydantic import BaseModel


# ---------- Tag ----------

class TagSummary(BaseModel):
    """Tag 요약 (목록용)."""

    tagNo: str
    description: Optional[str] = None
    systemName: Optional[str] = None
    packageName: Optional[str] = None
    manufactureName: Optional[str] = None


class TagDetail(TagSummary):
    """Tag 상세 (Attribute A~BD 등 모든 부가 속성 포함).

    attributes 는 원본 컬럼명을 키로 사용하여 사용자 친숙도 유지.
    """

    referenceDrawing: Optional[str] = None
    attributes: Dict[str, str] = {}


# ---------- Document ----------

class DocumentSummary(BaseModel):
    """문서/도면 요약."""

    documentNo: str
    documentName: Optional[str] = None
    revision: Optional[str] = None


class DocumentDetail(DocumentSummary):
    """문서 상세."""

    pdfAvailable: bool = False


# ---------- Manufacture ----------

class ManufactureDetail(BaseModel):
    """제조사 상세."""

    id: Optional[str] = None
    companyName: str
    industrySector: Optional[str] = None
    countryOrigin: Optional[str] = None
    vendorCode: Optional[str] = None
    phoneNumber: Optional[str] = None


# ---------- Hierarchy ----------

class SystemNode(BaseModel):
    """System 계층 노드."""

    systemName: str
    packageCount: int = 0


class PackageNode(BaseModel):
    """Package 계층 노드."""

    packageName: str
    systemName: Optional[str] = None
    tagCount: int = 0


# ---------- Search ----------

class SearchHit(BaseModel):
    """통합 검색 결과 1건."""

    hitType: str  # "tag" | "package" | "system" | "document"
    key: str
    label: str


# ---------- Diagnostics / Errors ----------

class DataStatus(BaseModel):
    """엑셀 적재 상태 (디버그/헬스체크용)."""

    rowCounts: Dict[str, int]
    errors: List[str] = []


class HealthStatus(BaseModel):
    """서버 상태 + 엑셀 로딩 상태 통합 응답."""

    status: str  # "ok" | "degraded"
    appName: str
    appVersion: str
    data: DataStatus


class ErrorBody(BaseModel):
    """에러 응답의 body 부분."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """통일 에러 응답 형식.

    예시:
    {
      "error": {
        "code": "TAG_NOT_FOUND",
        "message": "Tag 'P-9999' not found"
      }
    }
    """

    error: ErrorBody
