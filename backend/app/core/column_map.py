"""
엑셀 컬럼명 매핑.

엑셀 원본 컬럼명을 한 곳에서 관리한다.
원본 컬럼명이 바뀌면 이 파일만 수정하면 된다.

각 클래스는:
- 코드에서 참조할 상수 이름 = "원본 엑셀 컬럼명"
- REQUIRED: 검증 시 반드시 존재해야 하는 컬럼 목록
- ATTRIBUTE_PREFIX: 동적 컬럼(접두어 기반)이 있는 경우 prefix
"""
from typing import List


class TagColumns:
    """Tag_Register.xlsx 컬럼."""

    TAG = "Tag"
    DESCRIPTION = "Description"
    SYSTEM = "System"
    PACKAGE = "Package"
    REFERENCE_DRAWING = "Reference Drawing"
    MANUFACTURE_NAME = "Manufacture Name"

    # 필수 컬럼: 이 중 하나라도 빠지면 시스템 동작 불가
    REQUIRED: List[str] = [
        TAG,
        DESCRIPTION,
        SYSTEM,
        PACKAGE,
        REFERENCE_DRAWING,
        MANUFACTURE_NAME,
    ]

    # Attribute A ~ Attribute BD 까지의 동적 속성 컬럼은 prefix 로 식별
    ATTRIBUTE_PREFIX = "Attribute "


class DocumentColumns:
    """Document_List.xlsx 컬럼."""

    DOCUMENT_NUMBER = "Document Number"
    DOCUMENT_NAME = "Document Name"
    REVISION = "Revision"

    REQUIRED: List[str] = [DOCUMENT_NUMBER, DOCUMENT_NAME, REVISION]


class DocumentToTagColumns:
    """Document_to_Tag.xlsx 컬럼."""

    DOCUMENT_NUMBER = "Document Number"
    TAG = "Tag"

    REQUIRED: List[str] = [DOCUMENT_NUMBER, TAG]


class ManufactureColumns:
    """Manufacture_list.xlsx 컬럼.

    주의: Tag_Register 의 'Manufacture Name' 값과
    Manufacture_list 의 'Company_Name' 값이 조인 키이다.
    """

    ID = "ID"
    COMPANY_NAME = "Company_Name"
    INDUSTRY_SECTOR = "Industry_Sector"
    COUNTRY_ORIGIN = "Country_Origin"
    VENDOR_CODE = "Vendor_Code"
    PHONE_NUMBER = "Phone_Number"

    REQUIRED: List[str] = [
        ID,
        COMPANY_NAME,
        INDUSTRY_SECTOR,
        COUNTRY_ORIGIN,
        VENDOR_CODE,
        PHONE_NUMBER,
    ]
