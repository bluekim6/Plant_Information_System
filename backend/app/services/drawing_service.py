"""
Drawing(PDF) 서비스.

Document_Storage 폴더의 PDF 파일을 검색/스트리밍하는 책임을 진다.
실제 파일 응답은 api/routes/drawings.py에서 FileResponse로 처리한다.
"""
from pathlib import Path
from typing import Optional

from app.config.settings import getSettings
from app.utils.decrypt_fasoo import decrypt_fasoo_file


def resolveDrawingPath(documentNo: str) -> Optional[Path]:
    """문서번호 -> 실제 PDF 파일 절대경로 변환.

    파일명은 documentNo + '.pdf' 규칙을 가정한다.
    실제 매핑 규칙은 다음 단계에서 Document_List.xlsx의 파일명 컬럼에 맞춰 보강한다.

    회사 환경에서 PDF 도면에 Fasoo DRM 이 걸려 있을 수 있으므로, 응답으로
    내보내기 직전에 DRM 을 해제한다. 비(非) Windows/실패 시 원본 경로를 그대로 사용한다.
    """
    settings = getSettings()
    candidate = settings.drawingStoragePath / f"{documentNo}.pdf"
    if not candidate.exists():
        return None
    return decrypt_fasoo_file(candidate)
