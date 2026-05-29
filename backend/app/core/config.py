"""
환경설정 진입점.

실제 정의는 app.config.settings 에 있고, 여기서는 core 레이어의
표준 import 경로를 제공한다. (앞으로 모든 코드는 app.core.config 로
설정에 접근한다.)
"""
from app.config.settings import Settings, getSettings

__all__ = ["Settings", "getSettings"]
