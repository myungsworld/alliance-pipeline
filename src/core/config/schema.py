# schema.py - 설정 스키마 정의
# Pydantic을 사용해 설정값 검증

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class BrowserConfig(BaseModel):
    """브라우저 설정"""
    headless: bool = False
    timeout: int = 30
    proxy: Optional[str] = None
    user_agent: Optional[str] = None


class StorageConfig(BaseModel):
    """저장소 설정 - 어댑터 패턴으로 구현체 교체 가능"""
    type: str = "file"  # file, sqlite, mysql, mongodb, redis
    path: Optional[str] = "./data"
    connection_string: Optional[str] = None


class QueueConfig(BaseModel):
    """큐 설정 - 어댑터 패턴으로 구현체 교체 가능"""
    type: str = "memory"  # memory, rabbitmq, redis
    connection_string: Optional[str] = None


class SchedulerConfig(BaseModel):
    """스케줄러 설정"""
    type: str = "cron"  # cron, interval
    timezone: str = "Asia/Seoul"


class ServerConfig(BaseModel):
    """서버 설정"""
    host: str = "0.0.0.0"
    port: int = 8000


class Config(BaseModel):
    """
    전체 설정 스키마

    각 하위 설정들은 어댑터 패턴을 위한 type 필드를 가짐
    type에 따라 다른 구현체가 로드됨
    """
    env: str = "development"
    debug: bool = False
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    queue: QueueConfig = Field(default_factory=QueueConfig)
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)

    # 플러그인별 추가 설정 (동적)
    plugins: Dict[str, Any] = Field(default_factory=dict)
