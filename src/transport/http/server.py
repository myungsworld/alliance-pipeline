# server.py - FastAPI 서버
# REST API로 파이프라인 실행

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from src.core.logger import get_logger
from src.pipelines.base import PipelineRegistry

logger = get_logger(__name__)

app = FastAPI(
    title="Alliance Pipeline API",
    description="제휴 마케팅 자동화 파이프라인 API",
    version="0.1.0"
)


# ===== 요청/응답 모델 =====

class PipelineRunRequest(BaseModel):
    """파이프라인 실행 요청"""
    config: Optional[Dict[str, Any]] = None


class PipelineRunResponse(BaseModel):
    """파이프라인 실행 응답"""
    success: bool
    message: str
    task_id: Optional[str] = None


class ScrapeRequest(BaseModel):
    """크롤링 요청"""
    scraper: str
    keyword: Optional[str] = None
    max_items: int = 20


class HealthResponse(BaseModel):
    """헬스체크 응답"""
    status: str
    version: str


# ===== 엔드포인트 =====

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """헬스체크"""
    return HealthResponse(status="ok", version="0.1.0")


@app.get("/pipelines")
async def list_pipelines():
    """등록된 파이프라인 목록"""
    return {
        "pipelines": PipelineRegistry.list_available()
    }


@app.post("/pipelines/{name}/run", response_model=PipelineRunResponse)
async def run_pipeline(
    name: str,
    request: PipelineRunRequest,
    background_tasks: BackgroundTasks
):
    """
    파이프라인 실행

    백그라운드에서 실행하고 즉시 응답
    """
    try:
        pipeline = PipelineRegistry.get(name, request.config)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"파이프라인 '{name}' 없음"
        )

    # 백그라운드에서 실행
    import uuid
    task_id = str(uuid.uuid4())

    async def _run():
        logger.info(f"파이프라인 시작: {name} (task: {task_id})")
        result = await pipeline.execute()
        logger.info(f"파이프라인 완료: {name} (success: {result.success})")

    background_tasks.add_task(_run)

    return PipelineRunResponse(
        success=True,
        message=f"파이프라인 '{name}' 실행 시작됨",
        task_id=task_id
    )


@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    """
    크롤링 실행

    동기식으로 실행하고 결과 반환
    """
    from src.scrapers.base import ScraperRegistry

    try:
        scraper = ScraperRegistry.get(request.scraper)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"크롤러 '{request.scraper}' 없음"
        )

    result = await scraper.run(
        keyword=request.keyword,
        max_items=request.max_items
    )

    if result.success:
        return {
            "success": True,
            "items": result.items,
            "count": len(result.items)
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=result.error
        )


@app.get("/scrapers")
async def list_scrapers():
    """등록된 크롤러 목록"""
    from src.scrapers.base import ScraperRegistry
    return {
        "scrapers": ScraperRegistry.list_available()
    }


@app.get("/actions")
async def list_actions():
    """등록된 액션 목록"""
    from src.actions.base import ActionRegistry
    return {
        "actions": ActionRegistry.list_available()
    }
