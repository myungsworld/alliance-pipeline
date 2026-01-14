# mouse.py - 사람처럼 마우스 이동
# 직선이 아닌 자연스러운 곡선으로 이동

import random
import math
from typing import Tuple, Any

from selenium.webdriver.common.action_chains import ActionChains

from .delay import random_delay, click_delay


class HumanMouse:
    """
    사람처럼 마우스를 움직이는 클래스

    봇 탐지 시스템이 확인하는 것:
    - 마우스 이동 경로 (직선 vs 곡선)
    - 이동 속도 (일정 vs 가변)
    - 클릭 위치 (정확히 중앙 vs 약간 랜덤)

    이 클래스는 Bezier 곡선으로 자연스러운 경로 생성
    """

    def __init__(self, driver: Any):
        self._driver = driver
        self._current_x = 0
        self._current_y = 0

    async def move_to(self, x: int, y: int) -> None:
        """
        지정 좌표로 마우스 이동

        직선이 아닌 Bezier 곡선으로 이동
        """
        # 현재 위치에서 목표까지의 경로 생성
        points = self._generate_bezier_path(
            (self._current_x, self._current_y),
            (x, y)
        )

        # 경로를 따라 마우스 이동
        actions = ActionChains(self._driver)
        for point_x, point_y in points:
            actions.move_by_offset(
                point_x - self._current_x,
                point_y - self._current_y
            )
            self._current_x = point_x
            self._current_y = point_y

        actions.perform()
        self._current_x, self._current_y = x, y

    async def move_to_element(self, element: Any) -> None:
        """
        요소 위치로 마우스 이동

        정확히 중앙이 아닌 약간 랜덤한 위치로 이동
        """
        # 요소 위치와 크기
        rect = element.rect
        center_x = rect["x"] + rect["width"] / 2
        center_y = rect["y"] + rect["height"] / 2

        # 중앙에서 약간 벗어난 위치 (더 자연스러움)
        offset_x = random.uniform(-rect["width"] * 0.2, rect["width"] * 0.2)
        offset_y = random.uniform(-rect["height"] * 0.2, rect["height"] * 0.2)

        target_x = int(center_x + offset_x)
        target_y = int(center_y + offset_y)

        await self.move_to(target_x, target_y)

    async def click(self) -> None:
        """마우스 클릭"""
        await click_delay()
        ActionChains(self._driver).click().perform()

    async def double_click(self) -> None:
        """더블 클릭"""
        await click_delay()
        ActionChains(self._driver).double_click().perform()

    async def right_click(self) -> None:
        """우클릭"""
        await click_delay()
        ActionChains(self._driver).context_click().perform()

    def _generate_bezier_path(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        num_points: int = 20
    ) -> list:
        """
        Bezier 곡선 경로 생성

        시작점과 끝점 사이에 제어점을 추가하여
        자연스러운 곡선 경로 생성
        """
        x1, y1 = start
        x2, y2 = end

        # 거리 계산
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # 제어점 생성 (경로를 휘게 만듦)
        # 거리에 비례하여 휘어지는 정도 결정
        curve_amount = min(distance * 0.3, 100)

        # 랜덤한 방향으로 휘어짐
        angle = random.uniform(0, 2 * math.pi)
        ctrl_x = (x1 + x2) / 2 + math.cos(angle) * curve_amount
        ctrl_y = (y1 + y2) / 2 + math.sin(angle) * curve_amount

        # Quadratic Bezier curve 점들 생성
        points = []
        for i in range(num_points + 1):
            t = i / num_points

            # Bezier 공식
            x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * ctrl_x + t ** 2 * x2
            y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * ctrl_y + t ** 2 * y2

            points.append((int(x), int(y)))

        return points

    async def drag_and_drop(self, from_element: Any, to_element: Any) -> None:
        """드래그 앤 드롭"""
        await self.move_to_element(from_element)
        await click_delay()

        actions = ActionChains(self._driver)
        actions.click_and_hold()
        actions.perform()

        await random_delay(0.2, 0.5)

        await self.move_to_element(to_element)

        actions = ActionChains(self._driver)
        actions.release()
        actions.perform()
