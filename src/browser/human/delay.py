# delay.py - 자연스러운 딜레이
# 봇처럼 일정한 간격이 아닌 랜덤한 딜레이

import asyncio
import random


async def random_delay(min_sec: float = 0.5, max_sec: float = 2.0) -> None:
    """
    랜덤 딜레이

    사람은 일정한 속도로 행동하지 않음
    매번 다른 딜레이로 봇 탐지 우회
    """
    delay = random.uniform(min_sec, max_sec)
    await asyncio.sleep(delay)


async def typing_delay() -> None:
    """
    타이핑 딜레이

    사람의 타이핑 속도는 60-200ms 정도
    가끔 더 느린 경우도 있음 (생각하는 시간)
    """
    # 기본 타이핑 속도 (60-150ms)
    base_delay = random.uniform(0.06, 0.15)

    # 5% 확률로 더 긴 딜레이 (생각하는 시간)
    if random.random() < 0.05:
        base_delay += random.uniform(0.3, 0.8)

    await asyncio.sleep(base_delay)


async def click_delay() -> None:
    """
    클릭 전 딜레이

    마우스 이동 후 바로 클릭하지 않고
    약간의 인지 시간 후 클릭
    """
    await asyncio.sleep(random.uniform(0.1, 0.3))


async def page_load_delay() -> None:
    """
    페이지 로드 후 딜레이

    페이지 로드 후 바로 행동하지 않고
    내용을 읽는 시간 시뮬레이션
    """
    await asyncio.sleep(random.uniform(1.0, 3.0))


async def scroll_delay() -> None:
    """
    스크롤 간 딜레이

    연속 스크롤 시 사이 딜레이
    """
    await asyncio.sleep(random.uniform(0.5, 1.5))


def jitter(value: float, percentage: float = 0.2) -> float:
    """
    값에 랜덤 지터 추가

    Args:
        value: 기본값
        percentage: 변동 비율 (0.2 = ±20%)

    Returns:
        지터가 추가된 값
    """
    jitter_range = value * percentage
    return value + random.uniform(-jitter_range, jitter_range)
