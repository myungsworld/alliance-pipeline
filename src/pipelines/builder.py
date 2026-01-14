# builder.py - 파이프라인 빌더
# 체이닝 방식으로 파이프라인 구성

from typing import List, Callable, Any, Optional
from dataclasses import dataclass, field

from src.scrapers.base import Scraper
from src.publishers.base import Publisher, Content
from src.pipelines.base import Pipeline, PipelineResult, PipelineRegistry


# 변환 함수 타입
Transformer = Callable[[Any], Any]


@dataclass
class PipelineConfig:
    """파이프라인 설정"""
    scraper: Optional[Scraper] = None
    transformers: List[Transformer] = field(default_factory=list)
    publishers: List[Publisher] = field(default_factory=list)
    content_generator: Optional[Callable[[Any], Content]] = None


class BuiltPipeline(Pipeline):
    """빌더로 생성된 파이프라인"""

    def __init__(self, name: str, config: PipelineConfig):
        self._name = name
        self._config = config

    @property
    def name(self) -> str:
        return self._name

    async def run(self) -> PipelineResult:
        """파이프라인 실행"""
        errors = []
        items_processed = 0
        items_published = 0

        try:
            # 1. 데이터 수집
            if not self._config.scraper:
                return PipelineResult(success=False, errors=["스크래퍼 없음"])

            scrape_result = await self._config.scraper.run()
            if not scrape_result.success:
                return PipelineResult(
                    success=False,
                    errors=[scrape_result.error or "크롤링 실패"]
                )

            items = scrape_result.items
            items_processed = len(items)

            # 2. 데이터 변환
            for transformer in self._config.transformers:
                items = [transformer(item) for item in items]

            # 3. 콘텐츠 생성 및 발행
            if not self._config.content_generator:
                return PipelineResult(
                    success=True,
                    items_processed=items_processed,
                    metadata={"items": items}
                )

            for item in items:
                try:
                    content = self._config.content_generator(item)

                    # 모든 발행 채널에 발행
                    for publisher in self._config.publishers:
                        result = await publisher.run(content)
                        if result.success:
                            items_published += 1
                        else:
                            errors.append(f"{publisher.name}: {result.error}")

                except Exception as e:
                    errors.append(str(e))

            return PipelineResult(
                success=len(errors) == 0,
                items_processed=items_processed,
                items_published=items_published,
                errors=errors
            )

        except Exception as e:
            return PipelineResult(success=False, errors=[str(e)])


class PipelineBuilder:
    """
    파이프라인 빌더

    체이닝 방식으로 파이프라인 구성

    사용 예시:
        pipeline = (
            PipelineBuilder("coupang-to-blog")
            .source(CoupangDealScraper(min_discount=30))
            .transform(add_affiliate_link)
            .transform(format_price)
            .content(generate_blog_content)
            .publish(TistoryPublisher(...))
            .publish(TelegramPublisher(...))
            .build()
        )

        result = await pipeline.run()
    """

    def __init__(self, name: str):
        self._name = name
        self._config = PipelineConfig()

    def source(self, scraper: Scraper) -> "PipelineBuilder":
        """
        데이터 소스 설정

        Args:
            scraper: 크롤러 인스턴스
        """
        self._config.scraper = scraper
        return self

    def transform(self, transformer: Transformer) -> "PipelineBuilder":
        """
        변환 단계 추가

        여러 번 호출하여 체인 구성 가능

        Args:
            transformer: 변환 함수 (item -> item)
        """
        self._config.transformers.append(transformer)
        return self

    def content(self, generator: Callable[[Any], Content]) -> "PipelineBuilder":
        """
        콘텐츠 생성기 설정

        Args:
            generator: 아이템을 Content로 변환하는 함수
        """
        self._config.content_generator = generator
        return self

    def publish(self, publisher: Publisher) -> "PipelineBuilder":
        """
        발행 채널 추가

        여러 번 호출하여 멀티 채널 발행 가능

        Args:
            publisher: 발행 채널 인스턴스
        """
        self._config.publishers.append(publisher)
        return self

    def build(self) -> Pipeline:
        """파이프라인 생성"""
        return BuiltPipeline(self._name, self._config)

    def register(self) -> Pipeline:
        """파이프라인 생성 및 레지스트리에 등록"""
        pipeline = self.build()
        PipelineRegistry.register_with_name(self._name, type(pipeline))
        return pipeline
