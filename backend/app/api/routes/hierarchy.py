"""
계층 구조 라우터.

GET /api/hierarchy/systems                         - 전체 System 목록
GET /api/hierarchy/systems/{systemName}/packages   - System 하위 Package
GET /api/hierarchy/packages/{packageName}/tags     - Package 하위 Tag
"""
from typing import List

from fastapi import APIRouter

from app.models.schemas import PackageNode, SystemNode, TagSummary
from app.services.hierarchy_service import (
    listPackagesBySystem,
    listSystems,
    listTagsByPackage,
)

router = APIRouter(prefix="/api/hierarchy", tags=["hierarchy"])


@router.get("/systems", response_model=List[SystemNode])
def listSystemsRoute():
    """전체 System 목록."""
    return listSystems()


@router.get("/systems/{systemName}/packages", response_model=List[PackageNode])
def listPackagesRoute(systemName: str):
    """System 에 속한 Package 목록."""
    return listPackagesBySystem(systemName)


@router.get("/packages/{packageName}/tags", response_model=List[TagSummary])
def listTagsRoute(packageName: str):
    """Package 에 속한 Tag 목록."""
    return listTagsByPackage(packageName)
