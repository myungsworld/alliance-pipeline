# types.py - 이벤트 타입 정의
# 시스템 전체에서 사용되는 이벤트 타입들

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Event:
    """
    기본 이벤트 클래스

    모든 이벤트는 이 클래스를 상속하거나 직접 사용
    """
    type: str  # 이벤트 타입 (예: "scrape.complete", "publish.success")
    data: Dict[str, Any] = field(default_factory=dict)  # 이벤트 데이터
    timestamp: datetime = field(default_factory=datetime.now)  # 발생 시간
    source: Optional[str] = None  # 발생 모듈


# 사전 정의된 이벤트 타입들
class EventTypes:
    """이벤트 타입 상수"""
    # 스크래핑 관련
    SCRAPE_START = "scrape.start"
    SCRAPE_COMPLETE = "scrape.complete"
    SCRAPE_ERROR = "scrape.error"

    # 발행 관련
    PUBLISH_START = "publish.start"
    PUBLISH_SUCCESS = "publish.success"
    PUBLISH_ERROR = "publish.error"

    # 브라우저 관련
    BROWSER_OPEN = "browser.open"
    BROWSER_CLOSE = "browser.close"
    BROWSER_ERROR = "browser.error"

    # 액션 관련
    ACTION_START = "action.start"
    ACTION_COMPLETE = "action.complete"
    ACTION_ERROR = "action.error"

    # 파이프라인 관련
    PIPELINE_START = "pipeline.start"
    PIPELINE_COMPLETE = "pipeline.complete"
    PIPELINE_ERROR = "pipeline.error"
