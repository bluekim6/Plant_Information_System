#!/usr/bin/env python3
"""
설치/설정 검증 스크립트 (pre-flight check).

새 PC 에 클론한 직후, 서버를 띄우기 전에 환경이 올바른지 빠르게 확인한다.
각 항목을 PASS/FAIL 로 출력하고, 실패 시 해결 방법을 함께 보여준다.
하나라도 실패하면 종료 코드 1 을 반환한다.

실행 (저장소 루트에서):
    python verify_setup.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

# 저장소 루트 / backend 경로. 이 파일은 저장소 루트에 위치한다.
_REPO_ROOT = Path(__file__).resolve().parent
_BACKEND_DIR = _REPO_ROOT / "backend"

# 검증 결과 누적
_failures: list[str] = []


def _check(label: str, ok: bool, hint: str = "") -> bool:
    """한 항목의 PASS/FAIL 을 출력하고 실패 시 hint 를 보여준다."""
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}")
    if not ok:
        if hint:
            print(f"         -> {hint}")
        _failures.append(label)
    return ok


def checkPythonVersion() -> None:
    print("Python 버전")
    v = sys.version_info
    _check(
        f"Python {v.major}.{v.minor} (3.11 이상 필요)",
        v >= (3, 11),
        "Python 3.11 이상을 설치한 뒤 가상환경을 다시 만든다.",
    )


def checkDependencies() -> bool:
    """백엔드 의존성이 설치되어 있는지 확인한다. 모두 있어야 이후 검증 가능."""
    print("백엔드 의존성")
    # import 이름: pip 패키지명
    modules = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "pandas": "pandas",
        "openpyxl": "openpyxl",
        "pydantic": "pydantic",
        "pydantic_settings": "pydantic-settings",
        "dotenv": "python-dotenv",
    }
    allOk = True
    for mod, pkg in modules.items():
        ok = importlib.util.find_spec(mod) is not None
        _check(
            f"{pkg}",
            ok,
            "cd backend && pip install -r requirements.txt",
        )
        allOk = allOk and ok
    return allOk


def checkSettingsAndData() -> None:
    """설정 로드 + 엑셀/도면 경로 존재 + 실제 로딩(행 수) 을 검증한다."""
    print("설정 및 데이터 파일")

    # backend 를 import 경로에 추가하고, 있으면 .env 를 로드한다(없으면 기본값 사용).
    sys.path.insert(0, str(_BACKEND_DIR))
    from dotenv import load_dotenv

    envPath = _BACKEND_DIR / ".env"
    load_dotenv(envPath)
    if not envPath.exists():
        print("         (backend/.env 없음 -> 저장소 루트 기준 기본 경로 사용)")

    try:
        from app.core.config import getSettings

        settings = getSettings()
    except Exception as exc:  # noqa: BLE001
        _check(
            "설정(.env) 로드",
            False,
            f"backend/.env 형식 오류일 수 있음: {exc}",
        )
        return
    _check("설정(.env) 로드", True)

    dataPaths = [
        ("Tag_Register", settings.tagRegisterPath, False),
        ("Document_List", settings.documentListPath, False),
        ("Document_to_Tag", settings.documentToTagPath, False),
        ("Manufacture_list", settings.manufactureListPath, False),
        ("Document_Storage", settings.drawingStoragePath, True),
    ]
    for label, path, isDir in dataPaths:
        exists = path.is_dir() if isDir else path.is_file()
        _check(
            f"{label} 경로 존재: {path}",
            exists,
            "파일을 저장소 루트에 두거나 backend/.env 에서 해당 경로를 지정한다.",
        )

    # 도면 폴더에 PDF 가 하나라도 있는지(선택적 경고)
    storage = settings.drawingStoragePath
    if storage.is_dir():
        pdfCount = len(list(storage.glob("*.pdf")))
        _check(
            f"Document_Storage 내 PDF {pdfCount}개",
            pdfCount > 0,
            "도면 PDF 가 없으면 도면 뷰어가 비어 보인다(데이터 조회는 가능).",
        )

    # 엑셀이 실제로 파싱되고 행이 있는지 검증
    try:
        from app.data.excel_loader import preloadAll

        errors: list[str] = []
        rowCounts = preloadAll(onError=errors.append)
        for key, count in rowCounts.items():
            _check(f"엑셀 로딩 {key}: {count}행", count > 0)
        for err in errors:
            _check(f"엑셀 로딩 오류: {err}", False)
    except Exception as exc:  # noqa: BLE001
        _check("엑셀 로딩", False, str(exc))


def checkFrontend() -> None:
    """프론트엔드 의존성 설치 여부(경고 수준)."""
    print("프론트엔드")
    nodeModules = _REPO_ROOT / "frontend" / "node_modules"
    _check(
        "frontend/node_modules 설치됨",
        nodeModules.is_dir(),
        "cd frontend && npm install",
    )


def main() -> int:
    print("=" * 50)
    print(" Plant Information System - 설정 검증")
    print("=" * 50)

    checkPythonVersion()
    print()
    depsOk = checkDependencies()
    print()
    if depsOk:
        checkSettingsAndData()
    else:
        print("설정 및 데이터 파일")
        print("  (의존성 미설치로 건너뜀)")
    print()
    checkFrontend()

    print()
    print("=" * 50)
    if _failures:
        print(f" 결과: 실패 {len(_failures)}건 - 위 FAIL 항목을 해결한 뒤 다시 실행한다.")
        return 1
    print(" 결과: 모든 검증 통과 ✅  서버를 실행해도 됩니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
