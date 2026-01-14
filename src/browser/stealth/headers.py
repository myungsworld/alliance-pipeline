# headers.py - HTTP 헤더 위장
# 실제 브라우저와 동일한 헤더 생성

import random
from typing import Dict


# 실제 사용되는 User-Agent 목록 (정기적 업데이트 필요)
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",

    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",

    # Firefox Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",

    # Firefox Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",

    # Safari Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",

    # Edge Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]


def get_random_user_agent() -> str:
    """랜덤 User-Agent 반환"""
    return random.choice(USER_AGENTS)


def get_random_headers(referer: str = None) -> Dict[str, str]:
    """
    실제 브라우저와 유사한 HTTP 헤더 생성

    브라우저마다 헤더 순서와 값이 다름
    봇 탐지에서 헤더 패턴도 확인함
    """
    user_agent = get_random_user_agent()

    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none" if not referer else "same-origin",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    if referer:
        headers["Referer"] = referer

    # Chrome 특화 헤더
    if "Chrome" in user_agent:
        headers["sec-ch-ua"] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
        headers["sec-ch-ua-mobile"] = "?0"
        headers["sec-ch-ua-platform"] = '"Windows"' if "Windows" in user_agent else '"macOS"'

    return headers


def get_accept_header_for_type(content_type: str) -> str:
    """요청 타입에 맞는 Accept 헤더"""
    accept_map = {
        "html": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "json": "application/json, text/plain, */*",
        "image": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "css": "text/css,*/*;q=0.1",
        "js": "*/*",
    }
    return accept_map.get(content_type, "*/*")
