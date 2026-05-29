"""
Manufacture 데이터 접근 레이어.

조인 키 주의:
- Tag_Register 의 'Manufacture Name' 값
- Manufacture_list 의 'Company_Name' 값
이 같은 의미로 사용된다.
"""
from typing import List, Optional

import pandas as pd

from app.core.column_map import ManufactureColumns
from app.data.excel_loader import loadManufactureList
from app.models.schemas import ManufactureDetail


def _toDetail(row: pd.Series) -> ManufactureDetail:
    return ManufactureDetail(
        id=row.get(ManufactureColumns.ID) or None,
        companyName=row[ManufactureColumns.COMPANY_NAME],
        industrySector=row.get(ManufactureColumns.INDUSTRY_SECTOR) or None,
        countryOrigin=row.get(ManufactureColumns.COUNTRY_ORIGIN) or None,
        vendorCode=row.get(ManufactureColumns.VENDOR_CODE) or None,
        phoneNumber=row.get(ManufactureColumns.PHONE_NUMBER) or None,
    )


def findAllManufactures() -> List[ManufactureDetail]:
    """전체 제조사 목록."""
    df = loadManufactureList()
    return [_toDetail(row) for _, row in df.iterrows()]


def findManufactureByName(manufactureName: str) -> Optional[ManufactureDetail]:
    """제조사명(=Company_Name)으로 단건 조회.

    PRD 시나리오 D: Tag 화면에서 Manufacture Name 클릭 시 popup 으로
    상세 정보를 표시하기 위해 사용된다.
    """
    if not manufactureName:
        return None
    df = loadManufactureList()
    matched = df[df[ManufactureColumns.COMPANY_NAME] == manufactureName]
    if matched.empty:
        return None
    return _toDetail(matched.iloc[0])
