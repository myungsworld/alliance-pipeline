# write_post.py - 네이버 블로그 글쓰기 액션
# 사람처럼 자연스럽게 블로그 글 작성

from typing import Optional, Any, List
from selenium.webdriver.common.by import By

from src.actions.base import Action, ActionResult, ActionRegistry
from src.browser.human.delay import random_delay, page_load_delay


class NaverWritePost(Action):
    """
    네이버 블로그 글쓰기 액션

    사람처럼 자연스럽게 글 작성
    제목, 본문, 태그, 카테고리 지원

    사용법:
        write = NaverWritePost(
            title="글 제목",
            content="글 내용...",
            tags=["태그1", "태그2"],
            category="카테고리명"
        )
        result = await write.run(browser)

    주의: 로그인된 상태여야 함 (NaverLogin 먼저 실행)
    """

    def __init__(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        is_public: bool = True
    ):
        self._title = title
        self._content = content
        self._tags = tags or []
        self._category = category
        self._is_public = is_public

    @property
    def name(self) -> str:
        return "naver.write_post"

    async def execute(self, browser: Any) -> ActionResult:
        """글쓰기 실행"""
        try:
            # 1. 블로그 글쓰기 페이지로 이동
            await browser.goto("https://blog.naver.com/PostWriteForm.naver")
            await page_load_delay()

            # 2. 에디터 로드 대기
            await random_delay(2, 3)

            # 3. 제목 입력
            await self._input_title(browser)

            # 4. 본문 입력
            await self._input_content(browser)

            # 5. 태그 입력
            if self._tags:
                await self._input_tags(browser)

            # 6. 카테고리 선택
            if self._category:
                await self._select_category(browser)

            # 7. 공개 설정
            await self._set_visibility(browser)

            # 8. 발행
            await self._publish(browser)

            return ActionResult.ok({
                "title": self._title,
                "tags": self._tags,
            })

        except Exception as e:
            return ActionResult.fail(f"글쓰기 에러: {str(e)}")

    async def _input_title(self, browser: Any) -> None:
        """제목 입력"""
        # 네이버 블로그 에디터의 제목 입력란
        title_selector = ".se-title-text"
        await browser.human_click(title_selector)
        await random_delay(0.3, 0.5)
        await browser.human_type(title_selector, self._title, clear=True)
        await random_delay(0.5, 1)

    async def _input_content(self, browser: Any) -> None:
        """본문 입력"""
        # 에디터 본문 영역
        content_selector = ".se-text-paragraph"
        await browser.human_click(content_selector)
        await random_delay(0.3, 0.5)

        # 긴 내용은 여러 번 나눠서 입력 (더 자연스럽게)
        paragraphs = self._content.split("\n\n")
        for i, paragraph in enumerate(paragraphs):
            await browser.human_type(content_selector, paragraph)
            if i < len(paragraphs) - 1:
                # 엔터로 문단 구분
                await browser._keyboard.press_enter()
                await browser._keyboard.press_enter()
                await random_delay(0.5, 1)

    async def _input_tags(self, browser: Any) -> None:
        """태그 입력"""
        # 태그 입력 영역으로 스크롤
        await browser.human_scroll(300)
        await random_delay(0.5, 1)

        # 태그 입력란
        tag_selector = ".tag__input"
        for tag in self._tags:
            await browser.human_type(tag_selector, tag)
            await browser._keyboard.press_enter()
            await random_delay(0.3, 0.5)

    async def _select_category(self, browser: Any) -> None:
        """카테고리 선택"""
        # 카테고리 드롭다운 클릭
        category_btn = ".category_btn"
        await browser.human_click(category_btn)
        await random_delay(0.5, 1)

        # 카테고리 목록에서 찾아서 클릭
        # (실제 구현시 카테고리 목록 구조에 맞게 수정 필요)
        category_item = f"//a[contains(text(), '{self._category}')]"
        await browser.human_click(category_item, By.XPATH)
        await random_delay(0.3, 0.5)

    async def _set_visibility(self, browser: Any) -> None:
        """공개 설정"""
        if not self._is_public:
            # 비공개 설정 (필요시 구현)
            pass

    async def _publish(self, browser: Any) -> None:
        """발행"""
        publish_btn = ".publish_btn__text"
        await browser.human_click(publish_btn)
        await random_delay(1, 2)

        # 최종 발행 확인 버튼
        confirm_btn = ".confirm_btn"
        await browser.human_click(confirm_btn)
        await random_delay(2, 3)


# 레지스트리에 등록
ActionRegistry.register_with_name("naver.write_post", NaverWritePost)
