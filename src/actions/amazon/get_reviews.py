# get_reviews.py - 아마존 리뷰 수집 액션
# 상품 리뷰 데이터 크롤링

from typing import Any, List, Dict
from selenium.webdriver.common.by import By

from src.actions.base import Action, ActionResult, ActionRegistry
from src.browser.human.delay import random_delay, page_load_delay


class AmazonGetReviews(Action):
    """
    아마존 리뷰 수집 액션

    상품 URL에서 리뷰 데이터 수집
    별점, 제목, 내용, 날짜 등 추출

    사용법:
        reviews = AmazonGetReviews(
            product_url="https://www.amazon.com/dp/XXXXXXX",
            max_reviews=50
        )
        result = await reviews.run(browser)
        print(result.data["reviews"])
    """

    def __init__(
        self,
        product_url: str,
        max_reviews: int = 20,
        sort_by: str = "recent"  # recent, helpful
    ):
        self._product_url = product_url
        self._max_reviews = max_reviews
        self._sort_by = sort_by

    @property
    def name(self) -> str:
        return "amazon.get_reviews"

    async def execute(self, browser: Any) -> ActionResult:
        """리뷰 수집 실행"""
        try:
            # 1. 상품 페이지로 이동
            await browser.goto(self._product_url)
            await page_load_delay()

            # 2. 상품 정보 추출
            product_info = await self._get_product_info(browser)

            # 3. 리뷰 섹션으로 이동
            await self._navigate_to_reviews(browser)

            # 4. 정렬 설정
            await self._set_sort(browser)

            # 5. 리뷰 수집
            reviews = await self._collect_reviews(browser)

            return ActionResult.ok({
                "product": product_info,
                "reviews": reviews,
                "total_collected": len(reviews)
            })

        except Exception as e:
            return ActionResult.fail(f"리뷰 수집 에러: {str(e)}")

    async def _get_product_info(self, browser: Any) -> Dict:
        """상품 기본 정보 추출"""
        try:
            title = await browser.get_text("#productTitle")
            price = await browser.get_text(".a-price .a-offscreen")
            rating = await browser.get_text("#acrPopover .a-icon-alt")

            return {
                "title": title.strip() if title else "",
                "price": price.strip() if price else "",
                "rating": rating.strip() if rating else "",
                "url": self._product_url
            }
        except Exception:
            return {"url": self._product_url}

    async def _navigate_to_reviews(self, browser: Any) -> None:
        """리뷰 섹션으로 이동"""
        # "See all reviews" 링크 클릭
        try:
            reviews_link = "a[data-hook='see-all-reviews-link-foot']"
            await browser.human_click(reviews_link)
            await page_load_delay()
        except Exception:
            # 직접 리뷰 페이지 URL로 이동
            # /dp/ASIN -> /product-reviews/ASIN
            asin = self._product_url.split("/dp/")[-1].split("/")[0].split("?")[0]
            reviews_url = f"https://www.amazon.com/product-reviews/{asin}"
            await browser.goto(reviews_url)
            await page_load_delay()

    async def _set_sort(self, browser: Any) -> None:
        """정렬 설정"""
        if self._sort_by == "recent":
            # 최신순 정렬 선택
            try:
                sort_dropdown = "#sort-order-dropdown"
                await browser.human_click(sort_dropdown)
                await random_delay(0.5, 1)

                recent_option = "//a[contains(text(), 'Most recent')]"
                await browser.human_click(recent_option, By.XPATH)
                await page_load_delay()
            except Exception:
                pass  # 정렬 실패해도 계속 진행

    async def _collect_reviews(self, browser: Any) -> List[Dict]:
        """리뷰 수집"""
        reviews = []
        page = 1

        while len(reviews) < self._max_reviews:
            # 현재 페이지의 리뷰들 추출
            page_reviews = await self._extract_reviews_from_page(browser)
            reviews.extend(page_reviews)

            # 다음 페이지 확인
            if len(page_reviews) == 0:
                break

            # 다음 페이지로
            try:
                next_btn = ".a-pagination .a-last a"
                await browser.human_click(next_btn)
                await page_load_delay()
                page += 1

                # 사람처럼 스크롤하면서 읽는 척
                await browser.human_scroll(200)
                await random_delay(1, 2)
            except Exception:
                break  # 다음 페이지 없음

        return reviews[:self._max_reviews]

    async def _extract_reviews_from_page(self, browser: Any) -> List[Dict]:
        """현재 페이지에서 리뷰 추출"""
        reviews = []

        review_elements = await browser.find_all("[data-hook='review']")
        for element in review_elements:
            try:
                review = {
                    "rating": self._extract_rating(element),
                    "title": self._extract_text(element, "[data-hook='review-title']"),
                    "content": self._extract_text(element, "[data-hook='review-body']"),
                    "date": self._extract_text(element, "[data-hook='review-date']"),
                    "verified": self._is_verified(element),
                    "helpful_votes": self._extract_helpful_votes(element),
                }
                reviews.append(review)
            except Exception:
                continue

        return reviews

    def _extract_rating(self, element) -> str:
        """별점 추출"""
        try:
            rating_el = element.find_element(By.CSS_SELECTOR, "[data-hook='review-star-rating'] .a-icon-alt")
            return rating_el.get_attribute("textContent") or ""
        except Exception:
            return ""

    def _extract_text(self, element, selector: str) -> str:
        """텍스트 추출"""
        try:
            el = element.find_element(By.CSS_SELECTOR, selector)
            return el.text.strip()
        except Exception:
            return ""

    def _is_verified(self, element) -> bool:
        """인증된 구매 여부"""
        try:
            element.find_element(By.CSS_SELECTOR, "[data-hook='avp-badge']")
            return True
        except Exception:
            return False

    def _extract_helpful_votes(self, element) -> int:
        """도움이 됨 투표 수"""
        try:
            helpful_el = element.find_element(By.CSS_SELECTOR, "[data-hook='helpful-vote-statement']")
            text = helpful_el.text
            # "123 people found this helpful" 에서 숫자 추출
            import re
            match = re.search(r"(\d+)", text)
            return int(match.group(1)) if match else 0
        except Exception:
            return 0


# 레지스트리에 등록
ActionRegistry.register_with_name("amazon.get_reviews", AmazonGetReviews)
