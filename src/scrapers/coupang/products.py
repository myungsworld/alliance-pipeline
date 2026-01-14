# products.py - 쿠팡 상품 크롤러
# 카테고리별 상품 정보 수집

from typing import Optional, List, Dict, Any
import httpx
from bs4 import BeautifulSoup

from src.scrapers.base import Scraper, ScraperResult, ScraperRegistry
from src.browser.stealth.headers import get_random_headers


class CoupangProductScraper(Scraper):
    """
    쿠팡 상품 크롤러

    카테고리 또는 검색어로 상품 정보 수집
    브라우저 없이 HTTP 요청으로 빠르게 수집

    사용법:
        scraper = CoupangProductScraper(
            keyword="에어팟",
            max_items=50
        )
        result = await scraper.scrape()
    """

    def __init__(
        self,
        keyword: Optional[str] = None,
        category_id: Optional[str] = None,
        max_items: int = 20,
        sort: str = "saleCountDesc"  # saleCountDesc, priceAsc, priceDesc
    ):
        self._keyword = keyword
        self._category_id = category_id
        self._max_items = max_items
        self._sort = sort

    @property
    def name(self) -> str:
        return "coupang.products"

    async def scrape(self, **kwargs) -> ScraperResult:
        """상품 크롤링"""
        try:
            # URL 생성
            if self._keyword:
                url = f"https://www.coupang.com/np/search?q={self._keyword}&sorter={self._sort}"
            elif self._category_id:
                url = f"https://www.coupang.com/np/categories/{self._category_id}?sorter={self._sort}"
            else:
                return ScraperResult.fail("keyword 또는 category_id 필요")

            items = []
            page = 1

            while len(items) < self._max_items:
                page_url = f"{url}&page={page}"
                page_items = await self._scrape_page(page_url)

                if not page_items:
                    break

                items.extend(page_items)
                page += 1

            return ScraperResult.ok(
                items=items[:self._max_items],
                metadata={
                    "keyword": self._keyword,
                    "category_id": self._category_id,
                    "total_scraped": len(items)
                }
            )

        except Exception as e:
            return ScraperResult.fail(f"크롤링 에러: {str(e)}")

    async def _scrape_page(self, url: str) -> List[Dict[str, Any]]:
        """단일 페이지 크롤링"""
        headers = get_random_headers()

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=30)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = []

        # 상품 리스트 파싱
        product_elements = soup.select("li.search-product")
        for el in product_elements:
            item = self._parse_product(el)
            if item:
                items.append(item)

        return items

    def _parse_product(self, element) -> Optional[Dict[str, Any]]:
        """상품 정보 파싱"""
        try:
            # 상품 ID
            product_id = element.get("data-product-id")

            # 상품명
            name_el = element.select_one(".name")
            name = name_el.get_text(strip=True) if name_el else ""

            # 가격
            price_el = element.select_one(".price-value")
            price = price_el.get_text(strip=True) if price_el else ""
            price = price.replace(",", "")

            # 원가 (할인 전)
            original_price_el = element.select_one(".base-price")
            original_price = ""
            if original_price_el:
                original_price = original_price_el.get_text(strip=True).replace(",", "")

            # 할인율
            discount_el = element.select_one(".discount-percentage")
            discount = discount_el.get_text(strip=True) if discount_el else ""

            # 평점
            rating_el = element.select_one(".rating")
            rating = rating_el.get_text(strip=True) if rating_el else ""

            # 리뷰 수
            review_el = element.select_one(".rating-total-count")
            review_count = ""
            if review_el:
                review_count = review_el.get_text(strip=True).strip("()")

            # 상품 URL
            link_el = element.select_one("a.search-product-link")
            url = ""
            if link_el and link_el.get("href"):
                url = "https://www.coupang.com" + link_el.get("href")

            # 이미지 URL
            img_el = element.select_one("img.search-product-wrap-img")
            image_url = ""
            if img_el:
                image_url = img_el.get("src") or img_el.get("data-img-src") or ""
                if image_url.startswith("//"):
                    image_url = "https:" + image_url

            # 로켓배송 여부
            rocket = element.select_one(".badge.rocket") is not None

            return {
                "id": product_id,
                "name": name,
                "price": int(price) if price.isdigit() else 0,
                "original_price": int(original_price) if original_price.isdigit() else 0,
                "discount": discount,
                "rating": rating,
                "review_count": review_count,
                "url": url,
                "image_url": image_url,
                "rocket_delivery": rocket,
                "source": "coupang"
            }

        except Exception:
            return None


# 레지스트리에 등록
ScraperRegistry.register_with_name("coupang.products", CoupangProductScraper)
