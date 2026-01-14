# coupang_to_blog.py - 쿠팡 → 블로그 파이프라인
# 쿠팡 할인 상품을 티스토리 블로그에 자동 발행

from typing import Dict, Any, Optional

from src.scrapers.coupang import CoupangDealScraper
from src.publishers.tistory import TistoryPublisher
from src.publishers.telegram import TelegramPublisher
from src.publishers.base import Content
from src.pipelines.builder import PipelineBuilder
from src.pipelines.base import Pipeline


def add_affiliate_link(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    제휴 링크 추가 변환기

    쿠팡 파트너스 제휴 링크로 변환
    실제 사용시 파트너스 API로 딥링크 생성 필요
    """
    # TODO: 실제 쿠팡 파트너스 API 연동
    # 지금은 원본 URL 그대로 사용
    item["affiliate_url"] = item.get("url", "")
    return item


def format_price(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    가격 포맷팅 변환기

    숫자를 읽기 좋은 형태로 변환
    """
    price = item.get("price", 0)
    original = item.get("original_price", 0)

    item["price_formatted"] = f"{price:,}원"
    item["original_price_formatted"] = f"{original:,}원" if original else ""
    item["savings"] = f"{original - price:,}원" if original > price else ""

    return item


def generate_blog_content(item: Dict[str, Any]) -> Content:
    """
    블로그 글 콘텐츠 생성

    상품 정보를 블로그 글 형태로 변환
    """
    title = f"[{item.get('discount', '')}할인] {item.get('name', '')}"

    body_parts = [
        f"## {item.get('name', '')}",
        "",
        f"**가격**: ~~{item.get('original_price_formatted', '')}~~ → **{item.get('price_formatted', '')}**",
        "",
    ]

    if item.get("savings"):
        body_parts.append(f"**절약**: {item.get('savings')}")
        body_parts.append("")

    body_parts.extend([
        "### 상품 정보",
        "",
        f"- 할인율: {item.get('discount', '')}",
        f"- 로켓배송: {'O' if item.get('rocket_delivery') else 'X'}",
        "",
        f"[구매하기]({item.get('affiliate_url', '')})",
        "",
        "---",
        "*이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.*"
    ])

    body = "\n".join(body_parts)

    tags = ["쿠팡", "할인", "특가"]
    if item.get("rocket_delivery"):
        tags.append("로켓배송")

    return Content(
        title=title,
        body=body,
        tags=tags,
        images=[item.get("image_url", "")] if item.get("image_url") else [],
        metadata={"source_item": item}
    )


def generate_telegram_content(item: Dict[str, Any]) -> Content:
    """
    텔레그램 메시지 콘텐츠 생성

    짧고 임팩트 있는 형태로 변환
    """
    title = f"{item.get('discount', '')} 할인!"

    body_parts = [
        f"{item.get('name', '')}",
        "",
        f"💰 {item.get('original_price_formatted', '')} → {item.get('price_formatted', '')}",
        f"🏷️ {item.get('savings', '')} 절약!",
        "",
        f"🔗 {item.get('affiliate_url', '')}"
    ]

    body = "\n".join(body_parts)

    return Content(
        title=title,
        body=body,
        images=[item.get("image_url", "")] if item.get("image_url") else []
    )


def create_coupang_to_blog_pipeline(
    tistory_token: str,
    tistory_blog: str,
    telegram_token: Optional[str] = None,
    telegram_chat: Optional[str] = None,
    min_discount: int = 30,
    max_items: int = 5
) -> Pipeline:
    """
    쿠팡 → 블로그 파이프라인 생성

    Args:
        tistory_token: 티스토리 access_token
        tistory_blog: 티스토리 블로그 이름
        telegram_token: 텔레그램 봇 토큰 (선택)
        telegram_chat: 텔레그램 채널 ID (선택)
        min_discount: 최소 할인율
        max_items: 최대 처리 상품 수

    Returns:
        구성된 Pipeline
    """
    builder = (
        PipelineBuilder("coupang-to-blog")
        .source(CoupangDealScraper(
            deal_type="goldbox",
            min_discount=min_discount,
            max_items=max_items
        ))
        .transform(add_affiliate_link)
        .transform(format_price)
        .content(generate_blog_content)
        .publish(TistoryPublisher(
            access_token=tistory_token,
            blog_name=tistory_blog
        ))
    )

    # 텔레그램 추가 (선택)
    if telegram_token and telegram_chat:
        builder.publish(TelegramPublisher(
            bot_token=telegram_token,
            chat_id=telegram_chat
        ))

    return builder.build()
