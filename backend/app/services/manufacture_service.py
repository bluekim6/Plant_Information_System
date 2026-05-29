"""
Manufacture 서비스.

PRD 시나리오 D: Tag 화면에서 Manufacture Name 클릭 시
상세 정보를 popup 으로 표시.
"""
from typing import Optional

from app.models.schemas import ManufactureDetail
from app.repositories.manufacture_repository import findManufactureByName


def getManufactureDetail(manufactureName: str) -> Optional[ManufactureDetail]:
    """제조사 상세 정보를 반환한다."""
    return findManufactureByName(manufactureName)
