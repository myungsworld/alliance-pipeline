# pool.py - 브라우저 풀
# 여러 브라우저 인스턴스를 관리하여 병렬 작업 지원

import asyncio
from typing import Optional, List
from contextlib import asynccontextmanager

from .driver import StealthBrowser


class BrowserPool:
    """
    브라우저 풀

    여러 브라우저 인스턴스를 미리 생성해두고 재사용
    병렬 크롤링/자동화에 사용

    사용 예시:
        pool = BrowserPool(size=3)
        await pool.start()

        async with pool.acquire() as browser:
            await browser.goto("https://example.com")
            # ... 작업 ...

        await pool.shutdown()
    """

    def __init__(
        self,
        size: int = 3,
        headless: bool = True,
        proxy_list: Optional[List[str]] = None
    ):
        self._size = size
        self._headless = headless
        self._proxy_list = proxy_list or []

        # 사용 가능한 브라우저 큐
        self._available: asyncio.Queue[StealthBrowser] = asyncio.Queue()
        # 모든 브라우저 인스턴스
        self._browsers: List[StealthBrowser] = []
        # 초기화 여부
        self._started = False

    async def start(self) -> None:
        """풀 시작 - 브라우저 인스턴스들 생성"""
        if self._started:
            return

        for i in range(self._size):
            # 프록시 로테이션 (있으면)
            proxy = None
            if self._proxy_list:
                proxy = self._proxy_list[i % len(self._proxy_list)]

            browser = StealthBrowser(
                headless=self._headless,
                proxy=proxy
            )
            await browser.start()

            self._browsers.append(browser)
            await self._available.put(browser)

        self._started = True

    async def shutdown(self) -> None:
        """풀 종료 - 모든 브라우저 종료"""
        for browser in self._browsers:
            await browser.close()

        self._browsers.clear()
        self._available = asyncio.Queue()
        self._started = False

    @asynccontextmanager
    async def acquire(self):
        """
        브라우저 획득 (컨텍스트 매니저)

        사용 후 자동으로 풀에 반환됨
        """
        if not self._started:
            await self.start()

        browser = await self._available.get()
        try:
            yield browser
        finally:
            await self._available.put(browser)

    async def get(self) -> StealthBrowser:
        """
        브라우저 획득 (수동 반환 필요)

        반환: release() 호출 필요
        """
        if not self._started:
            await self.start()
        return await self._available.get()

    async def release(self, browser: StealthBrowser) -> None:
        """브라우저 반환"""
        await self._available.put(browser)

    @property
    def available_count(self) -> int:
        """사용 가능한 브라우저 수"""
        return self._available.qsize()

    @property
    def total_count(self) -> int:
        """전체 브라우저 수"""
        return len(self._browsers)
