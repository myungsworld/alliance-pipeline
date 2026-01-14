# deals.py - 쿠팡 할인 상품 크롤러
# 오늘의 특가, 골드박스 등 할인 상품 수집

from typing import List, Dict, Any
import os
from bs4 import BeautifulSoup

from src.scrapers.base import Scraper, ScraperResult, ScraperRegistry
from src.browser.engine.driver import StealthBrowser


class CoupangDealScraper(Scraper):
    """
    쿠팡 할인 상품 크롤러

    오늘의 특가, 골드박스 등 할인 상품 수집
    제휴 마케팅에 적합한 높은 할인율 상품 타겟

    사용법:
        scraper = CoupangDealScraper(deal_type="goldbox")
        result = await scraper.scrape()
    """

    # 할인 페이지 타입
    DEAL_TYPES = {
        "goldbox": "https://www.coupang.com/np/goldbox",
        "rocket_fresh": "https://www.coupang.com/np/campaigns/82",
        "travel": "https://www.coupang.com/np/coupangtravel",
    }

    def __init__(
        self,
        deal_type: str = "goldbox",
        min_discount: int = 0,  # 최소 할인율 필터
        max_items: int = 50
    ):
        self._deal_type = deal_type
        self._min_discount = min_discount
        self._max_items = max_items

    @property
    def name(self) -> str:
        return "coupang.deals"

    async def scrape(self, **kwargs) -> ScraperResult:
        """할인 상품 크롤링"""
        try:
            if self._deal_type not in self.DEAL_TYPES:
                return ScraperResult.fail(
                    f"지원하지 않는 deal_type: {self._deal_type}. "
                    f"사용 가능: {list(self.DEAL_TYPES.keys())}"
                )

            url = self.DEAL_TYPES[self._deal_type]
            items = await self._scrape_deals(url)

            # 최소 할인율 필터
            if self._min_discount > 0:
                items = [
                    item for item in items
                    if self._extract_discount_rate(item.get("discount", "")) >= self._min_discount
                ]

            return ScraperResult.ok(
                items=items[:self._max_items],
                metadata={
                    "deal_type": self._deal_type,
                    "min_discount": self._min_discount,
                    "total_scraped": len(items)
                }
            )

        except Exception as e:
            return ScraperResult.fail(f"크롤링 에러: {str(e)}")

    async def _scrape_deals(self, url: str) -> List[Dict[str, Any]]:
        """할인 페이지 크롤링 (StealthBrowser 사용)"""
        headless = os.environ.get("BROWSER_HEADLESS", "true").lower() == "true"

        async with StealthBrowser(headless=headless) as browser:
            await browser.goto(url)
            # 스크롤로 추가 상품 로드
            await browser.human_scroll(500)
            await browser.human_scroll(500)

            soup = BeautifulSoup(browser.page_source, "html.parser")

        items = []

        # 골드박스 상품 파싱
        product_elements = soup.select(".product-item, .baby-product-item")
        for el in product_elements:
            item = self._parse_deal_product(el)
            if item:
                items.append(item)

        return items

    def _parse_deal_product(self, element) -> Dict[str, Any]:
        """할인 상품 정보 파싱"""
        try:
            # 상품명
            name_el = element.select_one(".product-name, .title")
            name = name_el.get_text(strip=True) if name_el else ""

            # 현재 가격
            price_el = element.select_one(".sale-price, .price-value")
            price = ""
            if price_el:
                price = price_el.get_text(strip=True).replace(",", "").replace("원", "")

            # 원가
            original_el = element.select_one(".base-price, .origin-price")
            original_price = ""
            if original_el:
                original_price = original_el.get_text(strip=True).replace(",", "").replace("원", "")

            # 할인율
            discount_el = element.select_one(".discount-rate, .discount-percentage")
            discount = discount_el.get_text(strip=True) if discount_el else ""

            # URL
            link_el = element.select_one("a")
            url = ""
            if link_el and link_el.get("href"):
                href = link_el.get("href")
                if href.startswith("/"):
                    url = "https://www.coupang.com" + href
                else:
                    url = href

            # 이미지
            img_el = element.select_one("img")
            image_url = ""
            if img_el:
                image_url = img_el.get("src") or img_el.get("data-src") or ""
                if image_url.startswith("//"):
                    image_url = "https:" + image_url

            # 남은 수량 (있으면)
            stock_el = element.select_one(".progress-bar, .stock-count")
            remaining_stock = stock_el.get_text(strip=True) if stock_el else ""

            return {
                "name": name,
                "price": int(price) if price.isdigit() else 0,
                "original_price": int(original_price) if original_price.isdigit() else 0,
                "discount": discount,
                "discount_rate": self._extract_discount_rate(discount),
                "url": url,
                "image_url": image_url,
                "remaining_stock": remaining_stock,
                "deal_type": self._deal_type,
                "source": "coupang"
            }

        except Exception:
            return {}

    def _extract_discount_rate(self, discount_str: str) -> int:
        """할인율 문자열에서 숫자 추출"""
        import re
        match = re.search(r"(\d+)", discount_str)
        return int(match.group(1)) if match else 0


# 레지스트리에 등록
ScraperRegistry.register_with_name("coupang.deals", CoupangDealScraper)
