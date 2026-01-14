# commands.py - CLI 명령어 정의
# 파이프라인, 스크래퍼, 액션 등 실행

import asyncio
import argparse
import sys
from typing import Optional

from src.core.config import ConfigLoader
from src.core.logger import get_logger
from src.pipelines.base import PipelineRegistry
from src.scrapers.base import ScraperRegistry
from src.actions.base import ActionRegistry


logger = get_logger(__name__)


def cli():
    """메인 CLI 엔트리포인트"""
    parser = argparse.ArgumentParser(
        description="Alliance Pipeline - 제휴 마케팅 자동화"
    )

    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # pipeline 명령어
    pipeline_parser = subparsers.add_parser("pipeline", help="파이프라인 실행")
    pipeline_parser.add_argument("name", help="파이프라인 이름")
    pipeline_parser.add_argument("--config", "-c", help="설정 파일 경로")

    # scrape 명령어
    scrape_parser = subparsers.add_parser("scrape", help="크롤러 실행")
    scrape_parser.add_argument("name", help="크롤러 이름")
    scrape_parser.add_argument("--keyword", "-k", help="검색 키워드")
    scrape_parser.add_argument("--max", "-m", type=int, default=20, help="최대 아이템 수")
    scrape_parser.add_argument("--output", "-o", help="출력 파일 경로")

    # action 명령어
    action_parser = subparsers.add_parser("action", help="브라우저 액션 실행")
    action_parser.add_argument("name", help="액션 이름")
    action_parser.add_argument("--headless", action="store_true", help="헤드리스 모드")

    # server 명령어
    server_parser = subparsers.add_parser("server", help="API 서버 실행")
    server_parser.add_argument("--port", "-p", type=int, default=8000, help="포트")
    server_parser.add_argument("--host", default="0.0.0.0", help="호스트")

    # scheduler 명령어
    scheduler_parser = subparsers.add_parser("scheduler", help="스케줄러 실행")

    # list 명령어
    list_parser = subparsers.add_parser("list", help="등록된 플러그인 목록")
    list_parser.add_argument(
        "type",
        choices=["pipelines", "scrapers", "actions", "publishers"],
        help="플러그인 타입"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 명령어 실행
    if args.command == "pipeline":
        asyncio.run(run_pipeline(args.name, args.config))
    elif args.command == "scrape":
        asyncio.run(run_scraper(args.name, args.keyword, args.max, args.output))
    elif args.command == "action":
        asyncio.run(run_action(args.name, args.headless))
    elif args.command == "server":
        run_server(args.host, args.port)
    elif args.command == "scheduler":
        asyncio.run(run_scheduler())
    elif args.command == "list":
        list_plugins(args.type)


async def run_pipeline(name: str, config_path: Optional[str] = None):
    """파이프라인 실행"""
    logger.info(f"파이프라인 실행: {name}")

    try:
        # 설정 로드
        config_loader = ConfigLoader(config_path or "./config")
        config = config_loader.load()

        # 파이프라인 가져오기
        pipeline = PipelineRegistry.get(name)
        pipeline.initialize(config)

        # 실행
        result = await pipeline.execute()

        if result.success:
            logger.info(f"완료! 처리: {result.items_processed}, 발행: {result.items_published}")
        else:
            logger.error(f"실패: {result.errors}")

    except KeyError:
        logger.error(f"파이프라인 '{name}' 없음. 'list pipelines'로 확인하세요.")
    except Exception as e:
        logger.error(f"에러: {e}")


async def run_scraper(name: str, keyword: Optional[str], max_items: int, output: Optional[str]):
    """크롤러 실행"""
    logger.info(f"크롤러 실행: {name}")

    try:
        scraper = ScraperRegistry.get(name)
        result = await scraper.run(keyword=keyword, max_items=max_items)

        if result.success:
            logger.info(f"완료! {len(result.items)}개 수집")

            # 출력
            if output:
                import json
                with open(output, "w", encoding="utf-8") as f:
                    json.dump(result.items, f, ensure_ascii=False, indent=2)
                logger.info(f"저장됨: {output}")
            else:
                for item in result.items[:5]:  # 처음 5개만 출력
                    logger.info(f"  - {item.get('name', '')[:50]}...")
        else:
            logger.error(f"실패: {result.error}")

    except KeyError:
        logger.error(f"크롤러 '{name}' 없음. 'list scrapers'로 확인하세요.")
    except Exception as e:
        logger.error(f"에러: {e}")


async def run_action(name: str, headless: bool):
    """브라우저 액션 실행"""
    logger.info(f"액션 실행: {name}")

    try:
        from src.browser import StealthBrowser

        action = ActionRegistry.get(name)

        async with StealthBrowser(headless=headless) as browser:
            result = await action.run(browser)

            if result.success:
                logger.info(f"완료! {result.data}")
            else:
                logger.error(f"실패: {result.error}")

    except KeyError:
        logger.error(f"액션 '{name}' 없음. 'list actions'로 확인하세요.")
    except Exception as e:
        logger.error(f"에러: {e}")


def run_server(host: str, port: int):
    """API 서버 실행"""
    logger.info(f"서버 시작: {host}:{port}")

    try:
        import uvicorn
        from src.transport.http.server import app

        uvicorn.run(app, host=host, port=port)
    except ImportError:
        logger.error("FastAPI/uvicorn 설치 필요: pip install fastapi uvicorn")


async def run_scheduler():
    """스케줄러 실행"""
    logger.info("스케줄러 시작")

    from src.core.scheduler import SchedulerRegistry

    scheduler = SchedulerRegistry.get("cron")
    await scheduler.start()

    # 종료 시그널 대기
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await scheduler.stop()
        logger.info("스케줄러 종료")


def list_plugins(plugin_type: str):
    """등록된 플러그인 목록 출력"""
    registries = {
        "pipelines": PipelineRegistry,
        "scrapers": ScraperRegistry,
        "actions": ActionRegistry,
    }

    if plugin_type not in registries:
        print(f"알 수 없는 타입: {plugin_type}")
        return

    registry = registries[plugin_type]
    plugins = registry.list_available()

    if plugins:
        print(f"\n등록된 {plugin_type}:")
        for name in plugins:
            print(f"  - {name}")
    else:
        print(f"\n등록된 {plugin_type} 없음")


if __name__ == "__main__":
    cli()
