#!/usr/bin/env python3
"""
run.py - 통합 실행 스크립트

사용법:
    # CLI 모드
    python scripts/run.py pipeline coupang-to-blog
    python scripts/run.py scrape coupang.deals --max 10
    python scripts/run.py action naver.login

    # 서버 모드
    python scripts/run.py server --port 8000

    # 스케줄러 모드
    python scripts/run.py scheduler

    # 플러그인 목록
    python scripts/run.py list pipelines
"""

import sys
from pathlib import Path

# 프로젝트 루트를 path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 플러그인 자동 로드
from src.scrapers.coupang import CoupangProductScraper, CoupangDealScraper
from src.publishers.tistory import TistoryPublisher
from src.publishers.telegram import TelegramPublisher
from src.actions.naver import NaverLogin, NaverWritePost
from src.actions.amazon import AmazonGetReviews

# CLI 실행
from src.transport.cli.commands import cli

if __name__ == "__main__":
    cli()
