# base.py - 큐 인터페이스
# 어댑터 패턴: 이 인터페이스만 구현하면 어떤 큐든 교체 가능

from abc import abstractmethod
from typing import Any, Optional, Callable, Awaitable

from ..registry.plugin import Plugin, PluginRegistry


class Queue(Plugin):
    """
    메시지 큐 인터페이스 (어댑터 패턴)

    구현체 예시:
    - MemoryQueue: 인메모리 큐 (단일 프로세스)
    - RedisQueue: Redis 기반 큐
    - RabbitMQQueue: RabbitMQ

    사용법:
        queue = QueueRegistry.get("memory")

        # 메시지 발행
        await queue.publish("pipeline-jobs", {"task": "scrape", "url": "..."})

        # 메시지 소비
        async def handler(message):
            print(f"처리: {message}")

        await queue.subscribe("pipeline-jobs", handler)
    """

    @abstractmethod
    async def publish(self, channel: str, message: Any) -> None:
        """
        메시지 발행

        Args:
            channel: 채널/큐 이름
            message: 발행할 메시지 (직렬화 가능한 객체)
        """
        pass

    @abstractmethod
    async def subscribe(
        self,
        channel: str,
        handler: Callable[[Any], Awaitable[None]]
    ) -> None:
        """
        메시지 구독

        Args:
            channel: 채널/큐 이름
            handler: 메시지 수신시 호출될 비동기 함수
        """
        pass

    @abstractmethod
    async def unsubscribe(self, channel: str) -> None:
        """구독 해제"""
        pass

    @abstractmethod
    async def get(self, channel: str, timeout: Optional[float] = None) -> Optional[Any]:
        """
        메시지 하나 가져오기 (동기식 소비)

        Args:
            channel: 채널/큐 이름
            timeout: 대기 시간 (초). None이면 즉시 반환

        Returns:
            메시지 (없으면 None)
        """
        pass

    @abstractmethod
    def size(self, channel: str) -> int:
        """채널의 대기중인 메시지 수"""
        pass


# 큐 레지스트리 (싱글톤)
QueueRegistry: PluginRegistry[Queue] = PluginRegistry()
