# scrapers/ - 크롤러 플러그인
# 각 사이트별 상품/데이터 크롤러

from .base import Scraper, ScraperResult, ScraperRegistry

__all__ = ["Scraper", "ScraperResult", "ScraperRegistry"]
