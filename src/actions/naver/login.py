# login.py - 네이버 로그인 액션
# 사람처럼 자연스럽게 로그인

from typing import Optional, Any
from selenium.webdriver.common.by import By

from src.actions.base import Action, ActionResult, ActionRegistry
from src.browser.engine.session import BrowserSession
from src.browser.human.delay import random_delay


class NaverLogin(Action):
    """
    네이버 로그인 액션

    사람처럼 자연스럽게 로그인 수행
    세션 저장/복원 지원

    사용법:
        login = NaverLogin(
            username="아이디",
            password="비밀번호"
        )
        result = await login.run(browser)
    """

    def __init__(
        self,
        username: str,
        password: str,
        save_session: bool = True
    ):
        self._username = username
        self._password = password
        self._save_session = save_session
        self._session = BrowserSession("naver")

    @property
    def name(self) -> str:
        return "naver.login"

    async def execute(self, browser: Any) -> ActionResult:
        """로그인 실행"""
        try:
            # 1. 기존 세션으로 로그인 시도
            if self._session.exists():
                await browser.goto("https://www.naver.com")
                self._session.load(browser)
                await browser.refresh()
                await random_delay(1, 2)

                # 로그인 상태 확인
                if await self._is_logged_in(browser):
                    return ActionResult.ok({"method": "session"})

            # 2. 로그인 페이지로 이동
            await browser.goto("https://nid.naver.com/nidlogin.login")
            await random_delay(1, 2)

            # 3. 아이디 입력
            await browser.human_type("#id", self._username)
            await random_delay(0.5, 1)

            # 4. 비밀번호 입력
            await browser.human_type("#pw", self._password)
            await random_delay(0.5, 1)

            # 5. 로그인 버튼 클릭
            await browser.human_click("#log\\.login")
            await random_delay(2, 4)

            # 6. 로그인 결과 확인
            if await self._is_logged_in(browser):
                # 세션 저장
                if self._save_session:
                    self._session.save(browser)
                return ActionResult.ok({"method": "credentials"})

            # 캡차나 2차 인증 필요할 수 있음
            return ActionResult.fail("로그인 실패 - 추가 인증 필요할 수 있음")

        except Exception as e:
            return ActionResult.fail(f"로그인 에러: {str(e)}")

    async def _is_logged_in(self, browser: Any) -> bool:
        """로그인 상태 확인"""
        try:
            # 네이버 메인에서 로그인 상태 확인
            await browser.goto("https://www.naver.com")
            await random_delay(1, 2)

            # 로그아웃 버튼이 있으면 로그인된 상태
            elements = await browser.find_all(".MyView-module__btn_logout___bsTOJ")
            return len(elements) > 0
        except Exception:
            return False


# 레지스트리에 등록
ActionRegistry.register_with_name("naver.login", NaverLogin)
