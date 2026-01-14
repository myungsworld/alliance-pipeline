# scroll.py - 사람처럼 스크롤
# 부드럽고 자연스러운 스크롤

import random
from typing import Any

from .delay import scroll_delay, random_delay


class HumanScroll:
    """
    사람처럼 스크롤하는 클래스

    봇 탐지 시스템이 확인하는 것:
    - 스크롤 속도 (일정 vs 가변)
    - 스크롤 패턴 (한 번에 vs 여러 번)
    - 스크롤 중간 멈춤 (내용 읽는 시간)

    이 클래스는 부드러운 스크롤 +
    중간중간 멈춤 시뮬레이션
    """

    def __init__(self, driver: Any):
        self._driver = driver

    async def smooth_scroll(self, amount: int) -> None:
        """
        부드러운 스크롤

        한 번에 확 스크롤하지 않고
        여러 번 나눠서 자연스럽게 스크롤

        Args:
            amount: 스크롤할 픽셀 (양수: 아래, 음수: 위)
        """
        # 스크롤을 여러 단계로 나눔
        steps = random.randint(3, 7)
        step_amount = amount // steps

        for i in range(steps):
            # 각 스텝마다 약간 다른 양 스크롤
            jittered_amount = step_amount + random.randint(-20, 20)

            self._driver.execute_script(
                f"window.scrollBy({{top: {jittered_amount}, behavior: 'smooth'}});"
            )

            # 스텝 사이 딜레이 (스크롤 애니메이션 시간)
            await random_delay(0.1, 0.3)

        # 5% 확률로 잠시 멈춤 (내용 읽는 시간)
        if random.random() < 0.05:
            await scroll_delay()

    async def scroll_to_element(self, element: Any) -> None:
        """
        요소가 화면에 보일 때까지 스크롤

        한 번에 점프하지 않고 부드럽게 이동
        """
        # 요소 위치 확인
        rect = element.rect
        current_scroll = self._driver.execute_script("return window.pageYOffset;")
        viewport_height = self._driver.execute_script("return window.innerHeight;")

        # 요소가 화면 중앙에 오도록 스크롤 양 계산
        target_scroll = rect["y"] - viewport_height / 2
        scroll_amount = target_scroll - current_scroll

        # 부드럽게 스크롤
        await self.smooth_scroll(int(scroll_amount))

        # 요소 근처에서 미세 조정
        await random_delay(0.3, 0.5)

    async def scroll_to_bottom(self) -> None:
        """페이지 맨 아래로 스크롤"""
        page_height = self._driver.execute_script(
            "return document.documentElement.scrollHeight;"
        )
        current_scroll = self._driver.execute_script("return window.pageYOffset;")
        viewport_height = self._driver.execute_script("return window.innerHeight;")

        remaining = page_height - current_scroll - viewport_height

        # 여러 번 나눠서 스크롤
        while remaining > 100:
            scroll_amount = min(random.randint(300, 600), remaining)
            await self.smooth_scroll(scroll_amount)
            await random_delay(0.5, 1.5)  # 중간 멈춤 (내용 읽는 시간)

            remaining -= scroll_amount

    async def scroll_to_top(self) -> None:
        """페이지 맨 위로 스크롤"""
        current_scroll = self._driver.execute_script("return window.pageYOffset;")
        await self.smooth_scroll(-current_scroll)

    async def random_scroll(self) -> None:
        """
        랜덤 스크롤

        사람이 페이지를 둘러보는 것처럼
        위아래로 랜덤하게 스크롤
        """
        # 랜덤한 방향과 양
        direction = random.choice([1, -1])
        amount = random.randint(100, 400) * direction

        await self.smooth_scroll(amount)

    async def scroll_with_read(self, read_time: float = 2.0) -> None:
        """
        읽으면서 스크롤

        조금 스크롤 → 읽는 시간 → 조금 스크롤 반복
        """
        # 3-5번 반복
        for _ in range(random.randint(3, 5)):
            await self.smooth_scroll(random.randint(200, 400))
            await random_delay(read_time * 0.5, read_time * 1.5)
