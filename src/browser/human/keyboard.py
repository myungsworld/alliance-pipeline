# keyboard.py - 사람처럼 타이핑
# 일정한 속도가 아닌 자연스러운 타이핑

import random
from typing import Any

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from .delay import typing_delay, random_delay


class HumanKeyboard:
    """
    사람처럼 타이핑하는 클래스

    봇 탐지 시스템이 확인하는 것:
    - 타이핑 속도 (일정 vs 가변)
    - 키 누름 시간
    - 오타 발생 여부

    이 클래스는 자연스러운 타이핑 속도 +
    가끔 오타 후 수정하는 패턴 시뮬레이션
    """

    def __init__(self, driver: Any):
        self._driver = driver

    async def type_text(
        self,
        text: str,
        typo_rate: float = 0.02,  # 오타 확률 2%
        fix_typos: bool = True
    ) -> None:
        """
        텍스트 타이핑

        Args:
            text: 타이핑할 텍스트
            typo_rate: 오타 확률 (0.02 = 2%)
            fix_typos: 오타 발생시 수정 여부
        """
        actions = ActionChains(self._driver)

        for char in text:
            # 오타 시뮬레이션
            if random.random() < typo_rate:
                # 잘못된 키 입력
                wrong_char = self._get_nearby_key(char)
                actions.send_keys(wrong_char)
                actions.perform()
                await typing_delay()

                if fix_typos:
                    # 잠시 후 인지하고 삭제
                    await random_delay(0.3, 0.6)
                    actions = ActionChains(self._driver)
                    actions.send_keys(Keys.BACKSPACE)
                    actions.perform()
                    await typing_delay()

            # 올바른 키 입력
            actions = ActionChains(self._driver)
            actions.send_keys(char)
            actions.perform()
            await typing_delay()

    async def press_key(self, key: str) -> None:
        """단일 키 입력"""
        actions = ActionChains(self._driver)
        actions.send_keys(key)
        actions.perform()
        await typing_delay()

    async def press_enter(self) -> None:
        """엔터 키"""
        await self.press_key(Keys.ENTER)

    async def press_tab(self) -> None:
        """탭 키"""
        await self.press_key(Keys.TAB)

    async def press_escape(self) -> None:
        """ESC 키"""
        await self.press_key(Keys.ESCAPE)

    async def select_all(self) -> None:
        """전체 선택 (Ctrl+A / Cmd+A)"""
        actions = ActionChains(self._driver)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
        actions.perform()
        await random_delay(0.1, 0.3)

    async def copy(self) -> None:
        """복사 (Ctrl+C / Cmd+C)"""
        actions = ActionChains(self._driver)
        actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL)
        actions.perform()
        await random_delay(0.1, 0.3)

    async def paste(self) -> None:
        """붙여넣기 (Ctrl+V / Cmd+V)"""
        actions = ActionChains(self._driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)
        actions.perform()
        await random_delay(0.1, 0.3)

    def _get_nearby_key(self, char: str) -> str:
        """
        키보드에서 가까운 키 반환 (오타 시뮬레이션용)

        실제 오타는 주로 인접한 키에서 발생
        """
        # 한글은 그대로 반환 (복잡함)
        if ord(char) > 127:
            return char

        # 영문 키보드 인접 키 맵
        nearby_keys = {
            'a': ['s', 'q', 'z'],
            'b': ['v', 'n', 'g', 'h'],
            'c': ['x', 'v', 'd', 'f'],
            'd': ['s', 'f', 'e', 'r', 'c', 'x'],
            'e': ['w', 'r', 'd', 's'],
            'f': ['d', 'g', 'r', 't', 'v', 'c'],
            'g': ['f', 'h', 't', 'y', 'b', 'v'],
            'h': ['g', 'j', 'y', 'u', 'n', 'b'],
            'i': ['u', 'o', 'k', 'j'],
            'j': ['h', 'k', 'u', 'i', 'm', 'n'],
            'k': ['j', 'l', 'i', 'o', 'm'],
            'l': ['k', 'o', 'p'],
            'm': ['n', 'j', 'k'],
            'n': ['b', 'm', 'h', 'j'],
            'o': ['i', 'p', 'k', 'l'],
            'p': ['o', 'l'],
            'q': ['w', 'a'],
            'r': ['e', 't', 'd', 'f'],
            's': ['a', 'd', 'w', 'e', 'x', 'z'],
            't': ['r', 'y', 'f', 'g'],
            'u': ['y', 'i', 'h', 'j'],
            'v': ['c', 'b', 'f', 'g'],
            'w': ['q', 'e', 'a', 's'],
            'x': ['z', 'c', 's', 'd'],
            'y': ['t', 'u', 'g', 'h'],
            'z': ['a', 'x'],
        }

        char_lower = char.lower()
        if char_lower in nearby_keys:
            wrong = random.choice(nearby_keys[char_lower])
            return wrong.upper() if char.isupper() else wrong

        return char
