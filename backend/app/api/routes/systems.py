"""
System 라우터.

GET /api/systems                          - 전체 System 목록
GET /api/systems/{system_name}/packages   - System 하위 Package 목록
"""
from typing import List

from fastapi import APIRouter

from app.core.exceptions import ResourceNotFoundError
from app.models.schemas import ErrorResponse, PackageNode, SystemNode
from app.services.hierarchy_service import listPackagesBySystem, listSystems

router = APIRouter(prefix="/api/systems", tags=["systems"])


@router.get(
    "",
    response_model=List[SystemNode],
    summary="전체 System 목록",
    responses={503: {"model": ErrorResponse}},
)
def listSystemsRoute() -> List[SystemNode]:
    """Tag_Register 에서 추출한 전체 System 목록과 각 System 의 Package 수 반환."""
    return listSystems()


@router.get(
    "/{systemName}/packages",
    response_model=List[PackageNode],
    summary="특정 System 하위 Package 목록",
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
def listSystemPackagesRoute(systemName: str) -> List[PackageNode]:
    """주어진 System 에 속한 Package 목록과 각 Package 의 Tag 수 반환."""
    packages = listPackagesBySystem(systemName)
    if not packages:
        raise ResourceNotFoundError(
            f"System '{systemName}' not found or has no packages",
            code="SYSTEM_NOT_FOUND",
        )
    return packages
