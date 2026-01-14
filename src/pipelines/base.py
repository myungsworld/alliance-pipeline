# base.py - 파이프라인 인터페이스
# 데이터 흐름을 연결하는 파이프라인 기본 클래스

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.core.registry.plugin import Plugin, PluginRegistry


@dataclass
class PipelineResult:
    """
    파이프라인 실행 결과
    """
    success: bool
    items_processed: int = 0
    items_published: int = 0
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class Pipeline(Plugin):
    """
    파이프라인 인터페이스 (어댑터 패턴)

    데이터 수집 → 변환 → 발행의 흐름을 정의
    각 단계를 연결하여 자동화된 워크플로우 구성

    구현 예시:
    - CoupangToBlogPipeline: 쿠팡 상품 → 블로그 글
    - DealAlertPipeline: 할인 상품 → 텔레그램 알림

    사용법:
        pipeline = CoupangToBlogPipeline()
        result = await pipeline.run()
    """

    @abstractmethod
    async def run(self) -> PipelineResult:
        """
        파이프라인 실행

        Returns:
            PipelineResult
        """
        pass

    async def before_run(self) -> None:
        """실행 전 hook"""
        pass

    async def after_run(self, result: PipelineResult) -> None:
        """실행 후 hook"""
        pass

    async def execute(self) -> PipelineResult:
        """파이프라인 실행 (hook 포함)"""
        await self.before_run()
        result = await self.run()
        await self.after_run(result)
        return result


# 파이프라인 레지스트리 (싱글톤)
PipelineRegistry: PluginRegistry[Pipeline] = PluginRegistry()
