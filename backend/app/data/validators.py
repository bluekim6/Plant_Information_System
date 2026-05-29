"""
엑셀 데이터 검증 모듈.

파일 존재 여부, 필수 컬럼 존재 여부 등 데이터 무결성을 검사한다.
검증 실패 시 사용자 친화적인 메시지를 가진 ExcelDataError 를 발생시킨다.
"""
from pathlib import Path
from typing import List

import pandas as pd


class ExcelDataError(Exception):
    """엑셀 데이터 로딩/검증 실패."""


def validateFileExists(filePath: Path, label: str) -> None:
    """엑셀 파일 존재 여부 확인.

    Args:
        filePath: 검사할 파일 경로
        label: 사용자에게 보여줄 파일 식별자 (예: 'Tag_Register')
    """
    if not filePath.exists():
        raise ExcelDataError(
            f"[{label}] 엑셀 파일을 찾을 수 없습니다.\n"
            f"  경로: {filePath}\n"
            f"  -> backend/.env 의 경로 설정을 확인하세요."
        )
    if not filePath.is_file():
        raise ExcelDataError(
            f"[{label}] 지정된 경로가 파일이 아닙니다: {filePath}"
        )


def validateRequiredColumns(
    df: pd.DataFrame, requiredColumns: List[str], label: str
) -> None:
    """DataFrame 에 필수 컬럼이 모두 존재하는지 확인."""
    missing = [c for c in requiredColumns if c not in df.columns]
    if missing:
        raise ExcelDataError(
            f"[{label}] 필수 컬럼이 누락되었습니다.\n"
            f"  누락 컬럼: {missing}\n"
            f"  실제 컬럼: {list(df.columns)}\n"
            f"  -> 엑셀 헤더가 변경되었다면 backend/app/core/column_map.py 를 수정하세요."
        )
