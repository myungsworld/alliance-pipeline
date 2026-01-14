# memory.py - 인메모리 큐
# 단일 프로세스용 간단한 큐 (개발/테스트용)

import asyncio
from collections import defaultdict
from typing import Any, Optional, Callable, Awaitable, Dict, List

from .base import Queue, QueueRegistry


class MemoryQueue(Queue):
    """
    인메모리 큐 구현체

    단일 프로세스에서만 동작하는 간단한 큐
    개발/테스트 또는 소규모 사용에 적합

    예시:
        queue = MemoryQueue()
        await queue.publish("jobs", {"task": "scrape"})
        message = await queue.get("jobs")
    """

    def __init__(self):
        # 채널별 메시지 큐
        self._queues: Dict[str, asyncio.Queue] = defaultdict(asyncio.Queue)
        # 채널별 구독 핸들러
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)
        # 구독 태스크
        self._tasks: Dict[str, asyncio.Task] = {}

    @property
    def name(self) -> str:
        return "memory"

    def initialize(self, config: Optional[Any] = None) -> None:
        """초기화 (메모리 큐는 특별한 초기화 불필요)"""
        pass

    def shutdown(self) -> None:
        """모든 구독 태스크 취소"""
        for task in self._tasks.values():
            task.cancel()
        self._tasks.clear()
        self._handlers.clear()

    async def publish(self, channel: str, message: Any) -> None:
        """메시지 발행"""
        await self._queues[channel].put(message)

        # 구독 핸들러가 있으면 직접 호출 (pub/sub 모드)
        for handler in self._handlers[channel]:
            try:
                await handler(message)
            except Exception as e:
                print(f"큐 핸들러 에러 [{channel}]: {e}")

    async def subscribe(
        self,
        channel: str,
        handler: Callable[[Any], Awaitable[None]]
    ) -> None:
        """메시지 구독"""
        self._handlers[channel].append(handler)

        # 백그라운드에서 큐 소비 태스크 시작
        if channel not in self._tasks:
            self._tasks[channel] = asyncio.create_task(
                self._consume_loop(channel)
            )

    async def _consume_loop(self, channel: str) -> None:
        """백그라운드 큐 소비 루프"""
        while True:
            try:
                message = await self._queues[channel].get()
                for handler in self._handlers[channel]:
                    try:
                        await handler(message)
                    except Exception as e:
                        print(f"큐 핸들러 에러 [{channel}]: {e}")
            except asyncio.CancelledError:
                break

    async def unsubscribe(self, channel: str) -> None:
        """구독 해제"""
        self._handlers[channel].clear()
        if channel in self._tasks:
            self._tasks[channel].cancel()
            del self._tasks[channel]

    async def get(self, channel: str, timeout: Optional[float] = None) -> Optional[Any]:
        """메시지 하나 가져오기"""
        try:
            if timeout is None:
                # 즉시 반환 (없으면 None)
                return self._queues[channel].get_nowait()
            else:
                # 타임아웃까지 대기
                return await asyncio.wait_for(
                    self._queues[channel].get(),
                    timeout=timeout
                )
        except (asyncio.QueueEmpty, asyncio.TimeoutError):
            return None

    def size(self, channel: str) -> int:
        """대기중인 메시지 수"""
        return self._queues[channel].qsize()


# 레지스트리에 등록
QueueRegistry.register_with_name("memory", MemoryQueue)
