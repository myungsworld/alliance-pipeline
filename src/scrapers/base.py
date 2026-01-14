# base.py - 크롤러 인터페이스
# 모든 크롤러의 기본 클래스

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.core.registry.plugin import Plugin, PluginRegistry


@dataclass
class ScraperResult:
    """
    크롤러 실행 결과

    모든 크롤러는 이 형식으로 결과 반환
    """
    success: bool
    items: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def ok(cls, items: List[Dict], metadata: Dict = None) -> "ScraperResult":
        """성공 결과 생성"""
        return cls(success=True, items=items, metadata=metadata or {})

    @classmethod
    def fail(cls, error: str) -> "ScraperResult":
        """실패 결과 생성"""
        return cls(success=False, error=error)


class Scraper(Plugin):
    """
    크롤러 인터페이스 (어댑터 패턴)

    각 사이트별 크롤러를 구현
    같은 인터페이스로 다른 사이트 크롤러 교체 가능

    구현 예시:
    - CoupangProductScraper: 쿠팡 상품 정보
    - CoupangDealScraper: 쿠팡 할인 상품
    - AliexpressScraper: 알리익스프레스 상품

    사용법:
        scraper = CoupangProductScraper(category="가전")
        result = await scraper.scrape()
        for item in result.items:
            print(item["title"], item["price"])
    """

    @abstractmethod
    async def scrape(self, **kwargs) -> ScraperResult:
        """
        크롤링 실행

        Returns:
            ScraperResult (성공/실패 + 아이템 리스트)
        """
        pass

    async def before_scrape(self) -> None:
        """
        크롤링 전 hook

        오버라이드하여 사전 작업 수행
        예: 브라우저 세션 준비, 로그인 등
        """
        pass

    async def after_scrape(self, result: ScraperResult) -> None:
        """
        크롤링 후 hook

        오버라이드하여 후처리 수행
        예: 데이터 저장, 통계 로깅 등
        """
        pass

    async def run(self, **kwargs) -> ScraperResult:
        """
        크롤링 실행 (hook 포함)

        scrape() 직접 호출 대신 이 메서드 사용 권장
        """
        await self.before_scrape()
        result = await self.scrape(**kwargs)
        await self.after_scrape(result)
        return result


# 크롤러 레지스트리 (싱글톤)
ScraperRegistry: PluginRegistry[Scraper] = PluginRegistry()
