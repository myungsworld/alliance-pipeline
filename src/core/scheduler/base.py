# base.py - 스케줄러 인터페이스
# 어댑터 패턴: 이 인터페이스만 구현하면 어떤 스케줄러든 교체 가능

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Callable, Awaitable

from ..registry.plugin import Plugin, PluginRegistry


@dataclass
class Job:
    """스케줄된 작업 정보"""
    id: str
    name: str
    schedule: str  # cron 표현식 또는 interval
    handler: Callable[[], Awaitable[None]]
    enabled: bool = True


class Scheduler(Plugin):
    """
    스케줄러 인터페이스 (어댑터 패턴)

    구현체 예시:
    - CronScheduler: cron 표현식 기반
    - IntervalScheduler: 고정 간격 실행

    사용법:
        scheduler = SchedulerRegistry.get("cron")

        async def my_job():
            print("실행!")

        scheduler.add_job("my-job", "0 * * * *", my_job)  # 매시 정각
        await scheduler.start()
    """

    @abstractmethod
    def add_job(
        self,
        name: str,
        schedule: str,
        handler: Callable[[], Awaitable[None]]
    ) -> str:
        """
        작업 추가

        Args:
            name: 작업 이름
            schedule: 스케줄 표현식 (cron 또는 interval)
            handler: 실행할 비동기 함수

        Returns:
            작업 ID
        """
        pass

    @abstractmethod
    def remove_job(self, job_id: str) -> bool:
        """작업 제거"""
        pass

    @abstractmethod
    def pause_job(self, job_id: str) -> bool:
        """작업 일시정지"""
        pass

    @abstractmethod
    def resume_job(self, job_id: str) -> bool:
        """작업 재개"""
        pass

    @abstractmethod
    async def start(self) -> None:
        """스케줄러 시작"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """스케줄러 정지"""
        pass

    @abstractmethod
    def list_jobs(self) -> list[Job]:
        """등록된 작업 목록"""
        pass


# 스케줄러 레지스트리 (싱글톤)
SchedulerRegistry: PluginRegistry[Scheduler] = PluginRegistry()
