# rotator.py - 프록시 로테이션
# 자동으로 프록시를 돌려가며 사용

import random
from typing import Optional, List
from datetime import datetime, timedelta

from .manager import ProxyManager, Proxy


class ProxyRotator:
    """
    프록시 로테이터

    요청마다 다른 프록시 사용하여 차단 회피

    로테이션 전략:
    - round_robin: 순서대로 돌아가며 사용
    - random: 랜덤하게 선택
    - least_used: 가장 적게 사용된 프록시 선택
    - fastest: 가장 빠른 프록시 우선

    사용 예시:
        rotator = ProxyRotator(manager, strategy="random")
        proxy = rotator.next()  # 다음 프록시 가져오기
    """

    def __init__(
        self,
        manager: ProxyManager,
        strategy: str = "round_robin",
        cooldown_seconds: int = 0
    ):
        self._manager = manager
        self._strategy = strategy
        self._cooldown = timedelta(seconds=cooldown_seconds)

        # Round robin용 인덱스
        self._current_index = 0
        # 최근 사용 시간 기록
        self._last_used: dict = {}

    def next(self) -> Optional[Proxy]:
        """
        다음 프록시 가져오기

        Returns:
            Proxy 또는 None (사용 가능한 프록시 없음)
        """
        available = self._get_available_proxies()
        if not available:
            return None

        if self._strategy == "round_robin":
            return self._round_robin(available)
        elif self._strategy == "random":
            return self._random(available)
        elif self._strategy == "least_used":
            return self._least_used(available)
        elif self._strategy == "fastest":
            return self._fastest(available)
        else:
            return self._round_robin(available)

    def _get_available_proxies(self) -> List[Proxy]:
        """쿨다운 고려한 사용 가능 프록시 목록"""
        now = datetime.now()
        available = []

        for proxy in self._manager.get_all_available():
            last_used = self._last_used.get(proxy.address)
            if last_used is None or (now - last_used) >= self._cooldown:
                available.append(proxy)

        return available

    def _mark_used(self, proxy: Proxy) -> None:
        """프록시 사용 시간 기록"""
        self._last_used[proxy.address] = datetime.now()

    def _round_robin(self, available: List[Proxy]) -> Proxy:
        """순서대로 선택"""
        proxy = available[self._current_index % len(available)]
        self._current_index += 1
        self._mark_used(proxy)
        return proxy

    def _random(self, available: List[Proxy]) -> Proxy:
        """랜덤 선택"""
        proxy = random.choice(available)
        self._mark_used(proxy)
        return proxy

    def _least_used(self, available: List[Proxy]) -> Proxy:
        """가장 적게 사용된 프록시 선택"""
        available.sort(key=lambda p: p.success_count + p.fail_count)
        proxy = available[0]
        self._mark_used(proxy)
        return proxy

    def _fastest(self, available: List[Proxy]) -> Proxy:
        """가장 빠른 프록시 선택"""
        # 응답 시간이 0인 것은 아직 측정 안 된 것
        measured = [p for p in available if p.avg_response_time > 0]
        if measured:
            measured.sort(key=lambda p: p.avg_response_time)
            proxy = measured[0]
        else:
            proxy = random.choice(available)

        self._mark_used(proxy)
        return proxy

    def reset(self) -> None:
        """로테이션 상태 초기화"""
        self._current_index = 0
        self._last_used.clear()
