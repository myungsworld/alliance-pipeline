# exceptions.py - 커스텀 예외 클래스들
# 각 모듈별로 구분된 예외를 정의하여 에러 핸들링을 명확하게 함


class PipelineError(Exception):
    """파이프라인 관련 기본 예외"""
    pass


class ConfigError(PipelineError):
    """설정 로드/검증 실패"""
    pass


class BrowserError(PipelineError):
    """브라우저 조작 관련 에러"""
    pass


class ScraperError(PipelineError):
    """크롤링/스크래핑 관련 에러"""
    pass


class PublisherError(PipelineError):
    """콘텐츠 발행 관련 에러"""
    pass


class ActionError(PipelineError):
    """브라우저 액션 실행 에러"""
    pass


class StorageError(PipelineError):
    """저장소 관련 에러"""
    pass


class QueueError(PipelineError):
    """큐 관련 에러"""
    pass


class TransformError(PipelineError):
    """데이터 변환 관련 에러"""
    pass
