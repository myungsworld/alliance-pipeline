# cron.py - Cron 기반 스케줄러
# cron 표현식으로 작업 스케줄링

import asyncio
import uuid
from datetime import datetime
from typing import Any, Optional, Callable, Awaitable, Dict

from .base import Scheduler, SchedulerRegistry, Job


def parse_cron_field(field: str, min_val: int, max_val: int) -> set:
    """cron 필드 파싱 (간단한 구현)"""
    if field == "*":
        return set(range(min_val, max_val + 1))

    if "/" in field:
        # */5 같은 형식
        base, step = field.split("/")
        step = int(step)
        if base == "*":
            return set(range(min_val, max_val + 1, step))

    if "-" in field:
        # 1-5 같은 범위
        start, end = map(int, field.split("-"))
        return set(range(start, end + 1))

    if "," in field:
        # 1,3,5 같은 리스트
        return set(map(int, field.split(",")))

    return {int(field)}


def cron_matches(cron_expr: str, dt: datetime) -> bool:
    """cron 표현식이 현재 시간과 매칭되는지 확인"""
    parts = cron_expr.split()
    if len(parts) != 5:
        return False

    minute, hour, day, month, weekday = parts

    checks = [
        (minute, dt.minute, 0, 59),
        (hour, dt.hour, 0, 23),
        (day, dt.day, 1, 31),
        (month, dt.month, 1, 12),
        (weekday, dt.weekday(), 0, 6),  # 0=월요일
    ]

    for field, current, min_val, max_val in checks:
        allowed = parse_cron_field(field, min_val, max_val)
        if current not in allowed:
            return False

    return True


class CronScheduler(Scheduler):
    """
    Cron 기반 스케줄러 구현체

    cron 표현식으로 작업 스케줄링
    분 단위로 체크하여 매칭되면 실행

    cron 표현식: "분 시 일 월 요일"
    예시:
        "* * * * *"     - 매 분
        "0 * * * *"     - 매시 정각
        "0 9 * * *"     - 매일 오전 9시
        "0 9 * * 1"     - 매주 월요일 오전 9시
        "*/5 * * * *"   - 5분마다
    """

    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None

    @property
    def name(self) -> str:
        return "cron"

    def initialize(self, config: Optional[Any] = None) -> None:
        """초기화"""
        pass

    def shutdown(self) -> None:
        """종료"""
        asyncio.create_task(self.stop())

    def add_job(
        self,
        name: str,
        schedule: str,
        handler: Callable[[], Awaitable[None]]
    ) -> str:
        """작업 추가"""
        job_id = str(uuid.uuid4())
        self._jobs[job_id] = Job(
            id=job_id,
            name=name,
            schedule=schedule,
            handler=handler,
            enabled=True
        )
        return job_id

    def remove_job(self, job_id: str) -> bool:
        """작업 제거"""
        if job_id in self._jobs:
            del self._jobs[job_id]
            return True
        return False

    def pause_job(self, job_id: str) -> bool:
        """작업 일시정지"""
        if job_id in self._jobs:
            self._jobs[job_id].enabled = False
            return True
        return False

    def resume_job(self, job_id: str) -> bool:
        """작업 재개"""
        if job_id in self._jobs:
            self._jobs[job_id].enabled = True
            return True
        return False

    async def start(self) -> None:
        """스케줄러 시작"""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        """스케줄러 정지"""
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None

    def list_jobs(self) -> list[Job]:
        """등록된 작업 목록"""
        return list(self._jobs.values())

    async def _run_loop(self) -> None:
        """메인 스케줄러 루프 (1분마다 체크)"""
        last_minute = -1

        while self._running:
            now = datetime.now()

            # 같은 분에 중복 실행 방지
            if now.minute != last_minute:
                last_minute = now.minute

                # 모든 작업 체크
                for job in self._jobs.values():
                    if not job.enabled:
                        continue

                    if cron_matches(job.schedule, now):
                        # 비동기로 작업 실행 (블로킹 방지)
                        asyncio.create_task(self._run_job(job))

            # 1초마다 체크 (분 변경 감지용)
            await asyncio.sleep(1)

    async def _run_job(self, job: Job) -> None:
        """작업 실행"""
        try:
            await job.handler()
        except Exception as e:
            print(f"스케줄러 작업 에러 [{job.name}]: {e}")


# 레지스트리에 등록
SchedulerRegistry.register_with_name("cron", CronScheduler)
