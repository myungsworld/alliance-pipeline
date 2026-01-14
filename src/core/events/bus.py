# bus.py - 이벤트 버스
# 발행-구독 패턴으로 모듈간 통신

import asyncio
from typing import Callable, Dict, List, Union
from .types import Event


# 이벤트 핸들러 타입 (동기/비동기 모두 지원)
EventHandler = Callable[[Event], Union[None, asyncio.Future]]


class EventBus:
    """
    이벤트 버스

    발행-구독 패턴으로 모듈간 느슨한 결합 구현
    어떤 모듈이 이벤트를 발행하면, 구독한 모든 핸들러가 호출됨

    사용 예:
        # 구독
        bus.subscribe("scrape.complete", lambda e: print(f"완료: {e.data}"))

        # 발행
        bus.publish(Event(type="scrape.complete", data={"count": 10}))

        # 와일드카드 구독
        bus.subscribe("scrape.*", handler)  # scrape.로 시작하는 모든 이벤트
    """

    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._wildcard_handlers: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """
        이벤트 구독

        Args:
            event_type: 이벤트 타입 (예: "scrape.complete")
                        와일드카드 지원 (예: "scrape.*")
            handler: 이벤트 발생시 호출될 함수
        """
        if event_type.endswith("*"):
            # 와일드카드 핸들러
            prefix = event_type[:-1]  # "scrape.*" -> "scrape."
            if prefix not in self._wildcard_handlers:
                self._wildcard_handlers[prefix] = []
            self._wildcard_handlers[prefix].append(handler)
        else:
            # 정확한 매칭 핸들러
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """이벤트 구독 해제"""
        if event_type.endswith("*"):
            prefix = event_type[:-1]
            if prefix in self._wildcard_handlers:
                self._wildcard_handlers[prefix].remove(handler)
        else:
            if event_type in self._handlers:
                self._handlers[event_type].remove(handler)

    def publish(self, event: Event) -> None:
        """
        이벤트 발행 (동기)

        Args:
            event: 발행할 이벤트
        """
        handlers = self._get_handlers(event.type)
        for handler in handlers:
            try:
                result = handler(event)
                # 비동기 핸들러면 태스크로 실행
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception as e:
                # 핸들러 에러가 다른 핸들러에 영향 주지 않도록
                print(f"이벤트 핸들러 에러 [{event.type}]: {e}")

    async def publish_async(self, event: Event) -> None:
        """
        이벤트 발행 (비동기)

        모든 핸들러가 완료될 때까지 대기
        """
        handlers = self._get_handlers(event.type)
        tasks = []
        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    tasks.append(result)
            except Exception as e:
                print(f"이벤트 핸들러 에러 [{event.type}]: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _get_handlers(self, event_type: str) -> List[EventHandler]:
        """이벤트 타입에 매칭되는 모든 핸들러 조회"""
        handlers = []

        # 정확한 매칭
        if event_type in self._handlers:
            handlers.extend(self._handlers[event_type])

        # 와일드카드 매칭
        for prefix, wildcard_handlers in self._wildcard_handlers.items():
            if event_type.startswith(prefix):
                handlers.extend(wildcard_handlers)

        return handlers

    def clear(self) -> None:
        """모든 구독 해제"""
        self._handlers.clear()
        self._wildcard_handlers.clear()


# 글로벌 이벤트 버스 인스턴스 (싱글톤처럼 사용)
event_bus = EventBus()
