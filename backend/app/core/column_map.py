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

    # 위 핵심 컬럼을 제외한 나머지 컬럼은 모두 동적 속성(attribute)으로 수집한다.
    # (예: EQUIPMENT CLASS, VENDOR, MODEL DESCRIPTION, P&ID NUMBER ...)
    # 원본 헤더가 추가/변경되어도 코드 수정 없이 그대로 보존된다.
    CORE: List[str] = REQUIRED


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

    원본 컬럼명 'Adress', 'Contract Person' 은 엑셀 헤더의 철자를 그대로 따른다.
    """

    ID = "ID"
    COMPANY_NAME = "Company_Name"
    ADDRESS = "Adress"
    TOWN = "Town"
    PROVINCE = "Province"
    PHONE_NUMBER = "Phone Number"
    EMAIL = "e-mail"
    WEBSITE = "Website"
    CONTACT_PERSON = "Contract Person"
    COMPANY_TYPE = "Company Type"

    REQUIRED: List[str] = [
        ID,
        COMPANY_NAME,
    ]
