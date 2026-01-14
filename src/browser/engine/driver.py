# driver.py - 스텔스 브라우저 드라이버
# undetected-chromedriver (amd64) / Selenium (arm64) 자동 선택

from typing import Optional, Any
import os
import platform

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..stealth.fingerprint import apply_fingerprint_mask
from ..stealth.webdriver_mask import mask_webdriver_properties
from ..human.mouse import HumanMouse
from ..human.keyboard import HumanKeyboard
from ..human.scroll import HumanScroll
from ..human.delay import random_delay


def _is_arm64() -> bool:
    """arm64 아키텍처인지 확인"""
    return platform.machine() in ("arm64", "aarch64")


class StealthBrowser:
    """
    스텔스 브라우저

    탐지 우회 기능:
    - undetected-chromedriver 기반
    - webdriver 속성 숨김
    - fingerprint 위장
    - 사람처럼 행동 (마우스, 키보드, 스크롤)

    사용 예시:
        async with StealthBrowser() as browser:
            await browser.goto("https://example.com")
            await browser.human_click("#button")
            await browser.human_type("#input", "텍스트")
    """

    def __init__(
        self,
        headless: bool = False,
        proxy: Optional[str] = None,
        user_agent: Optional[str] = None,
        timeout: int = 30
    ):
        self._headless = headless
        self._proxy = proxy
        self._user_agent = user_agent
        self._timeout = timeout
        self._driver: Optional[WebDriver] = None

        # 사람처럼 행동하는 헬퍼들
        self._mouse: Optional[HumanMouse] = None
        self._keyboard: Optional[HumanKeyboard] = None
        self._scroll: Optional[HumanScroll] = None

    async def __aenter__(self) -> "StealthBrowser":
        """컨텍스트 매니저 진입"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """컨텍스트 매니저 종료"""
        await self.close()

    async def start(self) -> None:
        """브라우저 시작"""
        if _is_arm64():
            await self._start_selenium()
        else:
            await self._start_undetected()

    async def _start_undetected(self) -> None:
        """undetected-chromedriver로 시작 (amd64용, 봇 탐지 우회)"""
        import undetected_chromedriver as uc

        options = uc.ChromeOptions()

        if self._headless:
            options.add_argument("--headless=new")
        if self._proxy:
            options.add_argument(f"--proxy-server={self._proxy}")
        if self._user_agent:
            options.add_argument(f"--user-agent={self._user_agent}")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-first-run")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        # Chrome 바이너리 경로
        chrome_binary = os.environ.get("CHROME_BIN")
        if not chrome_binary:
            for path in ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable"]:
                if os.path.exists(path):
                    chrome_binary = path
                    break

        self._driver = uc.Chrome(options=options, browser_executable_path=chrome_binary)
        self._driver.implicitly_wait(self._timeout)
        self._init_helpers()

    async def _start_selenium(self) -> None:
        """일반 Selenium으로 시작 (arm64용, 제한적)"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        options = Options()

        if self._headless:
            options.add_argument("--headless=new")
        if self._proxy:
            options.add_argument(f"--proxy-server={self._proxy}")
        if self._user_agent:
            options.add_argument(f"--user-agent={self._user_agent}")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-first-run")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # Chrome 바이너리 경로
        chrome_binary = os.environ.get("CHROME_BIN")
        if not chrome_binary:
            for path in ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium"]:
                if os.path.exists(path):
                    chrome_binary = path
                    break
        if chrome_binary:
            options.binary_location = chrome_binary

        # ChromeDriver 경로
        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
        if not chromedriver_path:
            for path in ["/usr/bin/chromedriver", "/usr/local/bin/chromedriver"]:
                if os.path.exists(path):
                    chromedriver_path = path
                    break

        if chromedriver_path:
            service = Service(executable_path=chromedriver_path)
            self._driver = webdriver.Chrome(service=service, options=options)
        else:
            self._driver = webdriver.Chrome(options=options)

        self._driver.implicitly_wait(self._timeout)
        self._init_helpers()

    def _init_helpers(self) -> None:
        """Human behavior 헬퍼 초기화"""
        # 추가 탐지 우회 적용
        mask_webdriver_properties(self._driver)
        apply_fingerprint_mask(self._driver)

        # 사람 행동 헬퍼 초기화
        self._mouse = HumanMouse(self._driver)
        self._keyboard = HumanKeyboard(self._driver)
        self._scroll = HumanScroll(self._driver)

    async def close(self) -> None:
        """브라우저 종료"""
        if self._driver:
            self._driver.quit()
            self._driver = None

    @property
    def driver(self) -> WebDriver:
        """원본 WebDriver 접근 (고급 사용자용)"""
        if not self._driver:
            raise RuntimeError("브라우저가 시작되지 않음")
        return self._driver

    # ===== 기본 네비게이션 =====

    async def goto(self, url: str) -> None:
        """페이지 이동"""
        await random_delay(0.5, 1.5)  # 이동 전 자연스러운 딜레이
        self._driver.get(url)
        await random_delay(1, 2)  # 페이지 로드 후 딜레이

    async def back(self) -> None:
        """뒤로 가기"""
        await random_delay(0.3, 0.8)
        self._driver.back()

    async def forward(self) -> None:
        """앞으로 가기"""
        await random_delay(0.3, 0.8)
        self._driver.forward()

    async def refresh(self) -> None:
        """새로고침"""
        await random_delay(0.3, 0.8)
        self._driver.refresh()

    # ===== 사람처럼 행동하는 메서드들 =====

    async def human_click(self, selector: str, by: By = By.CSS_SELECTOR) -> None:
        """
        사람처럼 클릭

        마우스를 자연스럽게 이동 후 클릭
        """
        element = self._wait_for_element(selector, by)
        await self._mouse.move_to_element(element)
        await random_delay(0.1, 0.3)
        await self._mouse.click()

    async def human_type(
        self,
        selector: str,
        text: str,
        by: By = By.CSS_SELECTOR,
        clear: bool = True
    ) -> None:
        """
        사람처럼 타이핑

        자연스러운 타이핑 속도 + 오타 시뮬레이션
        """
        element = self._wait_for_element(selector, by)
        await self._mouse.move_to_element(element)
        await self._mouse.click()
        await random_delay(0.2, 0.5)

        if clear:
            element.clear()

        await self._keyboard.type_text(text)

    async def human_scroll(self, amount: int = 300) -> None:
        """
        사람처럼 스크롤

        부드러운 스크롤 + 랜덤한 속도
        """
        await self._scroll.smooth_scroll(amount)

    async def human_scroll_to_element(
        self,
        selector: str,
        by: By = By.CSS_SELECTOR
    ) -> None:
        """요소가 보일 때까지 스크롤"""
        element = self._wait_for_element(selector, by)
        await self._scroll.scroll_to_element(element)

    # ===== 요소 탐색 =====

    def _wait_for_element(self, selector: str, by: By = By.CSS_SELECTOR):
        """요소가 나타날 때까지 대기"""
        return WebDriverWait(self._driver, self._timeout).until(
            EC.presence_of_element_located((by, selector))
        )

    async def find(self, selector: str, by: By = By.CSS_SELECTOR):
        """요소 찾기"""
        return self._wait_for_element(selector, by)

    async def find_all(self, selector: str, by: By = By.CSS_SELECTOR) -> list:
        """모든 매칭 요소 찾기"""
        return self._driver.find_elements(by, selector)

    async def get_text(self, selector: str, by: By = By.CSS_SELECTOR) -> str:
        """요소의 텍스트 가져오기"""
        element = self._wait_for_element(selector, by)
        return element.text

    async def get_attribute(
        self,
        selector: str,
        attribute: str,
        by: By = By.CSS_SELECTOR
    ) -> Optional[str]:
        """요소의 속성 가져오기"""
        element = self._wait_for_element(selector, by)
        return element.get_attribute(attribute)

    # ===== 유틸리티 =====

    async def screenshot(self, path: str) -> None:
        """스크린샷 저장"""
        self._driver.save_screenshot(path)

    async def execute_script(self, script: str, *args) -> Any:
        """JavaScript 실행"""
        return self._driver.execute_script(script, *args)

    @property
    def current_url(self) -> str:
        """현재 URL"""
        return self._driver.current_url

    @property
    def page_source(self) -> str:
        """페이지 소스"""
        return self._driver.page_source
