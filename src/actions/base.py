# base.py - 액션 인터페이스
# 모든 브라우저 액션의 기본 클래스

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime

from src.core.registry.plugin import Plugin, PluginRegistry


@dataclass
class ActionResult:
    """
    액션 실행 결과

    모든 액션은 이 형식으로 결과 반환
    """
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def ok(cls, data: Dict[str, Any] = None) -> "ActionResult":
        """성공 결과 생성"""
        return cls(success=True, data=data or {})

    @classmethod
    def fail(cls, error: str) -> "ActionResult":
        """실패 결과 생성"""
        return cls(success=False, error=error)


class Action(Plugin):
    """
    브라우저 액션 인터페이스 (어댑터 패턴)

    각 사이트별 자동화 액션을 구현
    같은 인터페이스로 다른 사이트 액션 교체 가능

    구현 예시:
    - NaverLogin: 네이버 로그인
    - NaverWritePost: 네이버 블로그 글쓰기
    - AmazonGetReviews: 아마존 리뷰 수집

    사용법:
        action = NaverWritePost(title="제목", content="내용")
        result = await action.execute(browser)
        if result.success:
            print(f"성공: {result.data}")
    """

    @abstractmethod
    async def execute(self, browser: Any) -> ActionResult:
        """
        액션 실행

        Args:
            browser: StealthBrowser 인스턴스

        Returns:
            ActionResult (성공/실패 + 데이터)
        """
        pass

    async def before_execute(self, browser: Any) -> None:
        """
        액션 실행 전 hook

        오버라이드하여 사전 작업 수행
        예: 로그인 확인, 페이지 이동 등
        """
        pass

    async def after_execute(self, browser: Any, result: ActionResult) -> None:
        """
        액션 실행 후 hook

        오버라이드하여 후처리 수행
        예: 스크린샷 저장, 로깅 등
        """
        pass

    async def run(self, browser: Any) -> ActionResult:
        """
        액션 실행 (hook 포함)

        execute() 직접 호출 대신 이 메서드 사용 권장
        """
        await self.before_execute(browser)
        result = await self.execute(browser)
        await self.after_execute(browser, result)
        return result


# 액션 레지스트리 (싱글톤)
ActionRegistry: PluginRegistry[Action] = PluginRegistry()
