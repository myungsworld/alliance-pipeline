# logger.py - 로깅 유틸리티
# 전체 프로젝트에서 일관된 로깅 포맷 제공

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    모듈별 로거 생성

    Args:
        name: 로거 이름 (보통 __name__ 사용)
        level: 로깅 레벨 (기본값: INFO)

    Returns:
        설정된 Logger 인스턴스
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level or logging.INFO)
    return logger
