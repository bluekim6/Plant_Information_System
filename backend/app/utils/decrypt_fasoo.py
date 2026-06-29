"""
Fasoo DRM 복호화 유틸.

회사(폐쇄망/운영) 환경에서는 엑셀·PDF 등 문서에 Fasoo DRM 보안이 걸려 있어
일반적인 파일 읽기(pandas.read_excel, FileResponse 등)가 실패한다.
파일을 읽기 직전에 `decrypt_fasoo_file()` 을 호출하여 현재 프로세스에
DRM 읽기 권한을 부여한 뒤 정상 경로로 파싱/서빙을 진행한다.

설계 원칙 (참조: creat_code.md):
- Windows 환경 전용 (`C:/Windows/System32/f_nxldr.dll` 사용).
- DRM 해제 실패 시 원본 파일 경로를 그대로 반환한다. (파싱/서빙 시도는 계속)
  => 따라서 macOS/Linux 개발 환경에서는 자동으로 no-op 가 되어 기존과 동일하게 동작한다.
- `EnableDRM()` 은 프로세스 단위로 한 번만 호출하면 되므로 결과를 캐싱한다.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from threading import Lock
from typing import Optional, Union

logger = logging.getLogger(__name__)

# Fasoo DRM 로더 DLL 경로 (Windows 전용)
_FASOO_DLL_PATH = "C:/Windows/System32/f_nxldr.dll"

# EnableDRM 은 프로세스당 1회만 시도하면 되므로 결과를 캐싱한다.
_drmEnabled: Optional[bool] = None
_drmLock = Lock()


def _enableDrmOnce() -> bool:
    """현재 프로세스에 Fasoo DRM 읽기 권한을 부여한다 (프로세스당 1회).

    Returns:
        True  - DRM 활성화 성공 (이후 DRM 파일을 정상 읽기 가능)
        False - Windows 가 아니거나 DLL 로드/활성화 실패 (no-op 처리)
    """
    global _drmEnabled

    if _drmEnabled is not None:
        return _drmEnabled

    with _drmLock:
        # lock 획득 사이에 다른 스레드가 먼저 설정했을 수 있다.
        if _drmEnabled is not None:
            return _drmEnabled

        # Windows 가 아니면 시도조차 하지 않는다 (개발 환경 no-op).
        if not sys.platform.startswith("win"):
            logger.info("Fasoo DRM: 비(非) Windows 환경 -> 복호화 건너뜀")
            _drmEnabled = False
            return _drmEnabled

        try:
            from ctypes import CDLL

            fasoo = CDLL(_FASOO_DLL_PATH)
            ret = fasoo.EnableDRM()
            if not ret:
                raise RuntimeError("EnableDRM() 이 실패(0) 를 반환했습니다")
            logger.info("Fasoo DRM: 프로세스 DRM 읽기 권한 활성화 성공")
            _drmEnabled = True
        except Exception as exc:  # noqa: BLE001 - 어떤 실패든 no-op 로 처리
            logger.warning("Fasoo DRM 해제 실패 (원본 경로로 진행): %s", exc)
            _drmEnabled = False

        return _drmEnabled


def decrypt_fasoo_file(uploaded_file_path: Union[str, Path]) -> Path:
    """파일을 읽기 직전에 호출하여 Fasoo DRM 을 해제한다.

    DRM 활성화에 성공하든 실패하든 **원본 파일 경로를 그대로 반환**한다.
    (DRM 활성화는 프로세스 권한을 여는 작업이며 별도 복호화 사본을 만들지 않는다.)
    실패 시에도 경로를 반환하므로 호출부는 분기 없이 정상 파싱을 이어가면 된다.

    Args:
        uploaded_file_path: 읽으려는 원본 파일 경로.

    Returns:
        읽기에 사용할 파일 경로 (항상 원본 경로).
    """
    path = Path(uploaded_file_path)
    _enableDrmOnce()
    return path
