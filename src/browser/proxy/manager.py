# manager.py - 프록시 매니저
# 프록시 목록 관리 및 상태 추적

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import httpx


@dataclass
class Proxy:
    """프록시 정보"""
    address: str  # "ip:port" 또는 "protocol://ip:port"
    protocol: str = "http"  # http, https, socks5
    username: Optional[str] = None
    password: Optional[str] = None
    country: Optional[str] = None

    # 상태 추적
    is_alive: bool = True
    last_check: Optional[datetime] = None
    fail_count: int = 0
    success_count: int = 0
    avg_response_time: float = 0.0

    @property
    def url(self) -> str:
        """프록시 URL 생성"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.address}"
        return f"{self.protocol}://{self.address}"


class ProxyManager:
    """
    프록시 매니저

    프록시 목록 관리 + 상태 추적 + 자동 제거

    사용 예시:
        manager = ProxyManager()
        manager.add_proxy("123.45.67.89:8080")
        manager.add_proxy("98.76.54.32:3128", protocol="socks5")

        # 사용 가능한 프록시 가져오기
        proxy = manager.get_available()

        # 결과 보고
        manager.report_success(proxy)
        manager.report_failure(proxy)
    """

    def __init__(self, max_fails: int = 3):
        self._proxies: Dict[str, Proxy] = {}
        self._max_fails = max_fails

    def add_proxy(
        self,
        address: str,
        protocol: str = "http",
        username: Optional[str] = None,
        password: Optional[str] = None,
        country: Optional[str] = None
    ) -> None:
        """프록시 추가"""
        proxy = Proxy(
            address=address,
            protocol=protocol,
            username=username,
            password=password,
            country=country
        )
        self._proxies[address] = proxy

    def add_proxies_from_list(self, proxy_list: List[str]) -> None:
        """
        문자열 리스트에서 프록시 추가

        형식: "ip:port" 또는 "protocol://ip:port"
        """
        for proxy_str in proxy_list:
            if "://" in proxy_str:
                protocol, address = proxy_str.split("://", 1)
            else:
                protocol = "http"
                address = proxy_str
            self.add_proxy(address, protocol)

    def get_available(self, country: Optional[str] = None) -> Optional[Proxy]:
        """
        사용 가능한 프록시 반환

        Args:
            country: 특정 국가 프록시만 필터 (선택)

        Returns:
            Proxy 또는 None
        """
        available = [
            p for p in self._proxies.values()
            if p.is_alive and p.fail_count < self._max_fails
        ]

        if country:
            available = [p for p in available if p.country == country]

        if not available:
            return None

        # 성공률 높은 프록시 우선
        available.sort(key=lambda p: p.success_count, reverse=True)
        return available[0]

    def get_all_available(self) -> List[Proxy]:
        """모든 사용 가능한 프록시 목록"""
        return [
            p for p in self._proxies.values()
            if p.is_alive and p.fail_count < self._max_fails
        ]

    def report_success(self, proxy: Proxy, response_time: float = 0.0) -> None:
        """프록시 사용 성공 보고"""
        if proxy.address in self._proxies:
            p = self._proxies[proxy.address]
            p.success_count += 1
            p.fail_count = 0  # 성공하면 실패 카운트 리셋
            p.last_check = datetime.now()

            # 평균 응답 시간 업데이트
            if p.avg_response_time == 0:
                p.avg_response_time = response_time
            else:
                p.avg_response_time = (p.avg_response_time + response_time) / 2

    def report_failure(self, proxy: Proxy) -> None:
        """프록시 사용 실패 보고"""
        if proxy.address in self._proxies:
            p = self._proxies[proxy.address]
            p.fail_count += 1
            p.last_check = datetime.now()

            # 최대 실패 횟수 초과시 비활성화
            if p.fail_count >= self._max_fails:
                p.is_alive = False

    def remove_dead(self) -> int:
        """죽은 프록시 제거"""
        dead = [addr for addr, p in self._proxies.items() if not p.is_alive]
        for addr in dead:
            del self._proxies[addr]
        return len(dead)

    async def check_proxy(self, proxy: Proxy, test_url: str = "http://httpbin.org/ip") -> bool:
        """
        프록시 동작 확인

        실제로 요청을 보내서 프록시가 작동하는지 테스트
        """
        try:
            async with httpx.AsyncClient(proxy=proxy.url, timeout=10) as client:
                start = datetime.now()
                response = await client.get(test_url)
                elapsed = (datetime.now() - start).total_seconds()

                if response.status_code == 200:
                    self.report_success(proxy, elapsed)
                    return True

        except Exception:
            pass

        self.report_failure(proxy)
        return False

    async def check_all(self, test_url: str = "http://httpbin.org/ip") -> Dict[str, bool]:
        """모든 프록시 확인"""
        results = {}
        for proxy in self._proxies.values():
            results[proxy.address] = await self.check_proxy(proxy, test_url)
        return results

    @property
    def count(self) -> int:
        """전체 프록시 수"""
        return len(self._proxies)

    @property
    def available_count(self) -> int:
        """사용 가능한 프록시 수"""
        return len(self.get_all_available())
