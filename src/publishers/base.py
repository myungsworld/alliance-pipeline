# base.py - 발행 채널 인터페이스
# 모든 발행 채널의 기본 클래스

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime

from src.core.registry.plugin import Plugin, PluginRegistry


@dataclass
class Content:
    """
    발행할 콘텐츠

    모든 발행 채널에서 공통으로 사용
    """
    title: str
    body: str
    tags: list = field(default_factory=list)
    images: list = field(default_factory=list)  # 이미지 URL 리스트
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PublishResult:
    """
    발행 결과

    모든 발행 채널은 이 형식으로 결과 반환
    """
    success: bool
    url: Optional[str] = None  # 발행된 콘텐츠 URL
    post_id: Optional[str] = None  # 플랫폼별 게시물 ID
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def ok(cls, url: str = None, post_id: str = None) -> "PublishResult":
        """성공 결과 생성"""
        return cls(success=True, url=url, post_id=post_id)

    @classmethod
    def fail(cls, error: str) -> "PublishResult":
        """실패 결과 생성"""
        return cls(success=False, error=error)


class Publisher(Plugin):
    """
    발행 채널 인터페이스 (어댑터 패턴)

    각 플랫폼별 발행 기능을 구현
    같은 인터페이스로 다른 플랫폼 교체 가능

    구현 예시:
    - TistoryPublisher: 티스토리 블로그
    - TelegramPublisher: 텔레그램 채널
    - DiscordPublisher: 디스코드 웹훅

    사용법:
        content = Content(title="제목", body="내용")
        publisher = TistoryPublisher(blog_name="myblog")
        result = await publisher.publish(content)
    """

    @abstractmethod
    async def publish(self, content: Content) -> PublishResult:
        """
        콘텐츠 발행

        Args:
            content: 발행할 콘텐츠

        Returns:
            PublishResult (성공/실패 + URL)
        """
        pass

    async def before_publish(self, content: Content) -> Content:
        """
        발행 전 hook

        오버라이드하여 콘텐츠 전처리
        예: 템플릿 적용, 이미지 업로드 등

        Returns:
            수정된 Content
        """
        return content

    async def after_publish(self, content: Content, result: PublishResult) -> None:
        """
        발행 후 hook

        오버라이드하여 후처리 수행
        예: 통계 기록, 알림 등
        """
        pass

    async def run(self, content: Content) -> PublishResult:
        """
        발행 실행 (hook 포함)

        publish() 직접 호출 대신 이 메서드 사용 권장
        """
        content = await self.before_publish(content)
        result = await self.publish(content)
        await self.after_publish(content, result)
        return result


# 발행 채널 레지스트리 (싱글톤)
PublisherRegistry: PluginRegistry[Publisher] = PluginRegistry()
