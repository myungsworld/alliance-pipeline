# plugin.py - 플러그인 시스템
# 모든 확장 가능한 컴포넌트의 기반 인터페이스

from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar, Generic, Optional, Any

T = TypeVar("T", bound="Plugin")


class Plugin(ABC):
    """
    플러그인 기본 인터페이스

    모든 교체 가능한 컴포넌트(Storage, Queue, Scraper, Publisher 등)가
    이 인터페이스를 상속받음

    어댑터 패턴: 같은 인터페이스를 구현하면 언제든 교체 가능
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """플러그인 고유 이름 (예: 'mysql', 'mongodb', 'naver')"""
        pass

    def initialize(self, config: Optional[Any] = None) -> None:
        """
        플러그인 초기화

        연결 설정, 리소스 할당 등 수행
        """
        pass

    def shutdown(self) -> None:
        """
        플러그인 종료

        연결 해제, 리소스 정리 등 수행
        """
        pass

    def health_check(self) -> bool:
        """플러그인 상태 확인"""
        return True


class PluginRegistry(Generic[T]):
    """
    플러그인 레지스트리

    같은 타입의 여러 구현체를 등록하고,
    이름으로 조회하여 사용

    사용 예:
        # 등록
        storage_registry = PluginRegistry[Storage]()
        storage_registry.register(FileStorage)
        storage_registry.register(MySQLStorage)
        storage_registry.register(MongoDBStorage)

        # 조회 및 사용
        storage = storage_registry.get("mysql")
    """

    def __init__(self):
        self._plugins: Dict[str, Type[T]] = {}
        self._instances: Dict[str, T] = {}

    def register(self, plugin_class: Type[T]) -> None:
        """
        플러그인 클래스 등록

        Args:
            plugin_class: Plugin을 상속한 클래스
        """
        # 임시 인스턴스로 이름 확인
        temp_instance = plugin_class.__new__(plugin_class)
        if hasattr(plugin_class, 'name') and isinstance(plugin_class.name, property):
            # property인 경우 기본값 사용하거나 클래스명 사용
            name = plugin_class.__name__.lower()
        else:
            name = getattr(temp_instance, 'name', plugin_class.__name__.lower())

        self._plugins[name] = plugin_class

    def register_with_name(self, name: str, plugin_class: Type[T]) -> None:
        """
        특정 이름으로 플러그인 클래스 등록

        Args:
            name: 플러그인 이름
            plugin_class: Plugin을 상속한 클래스
        """
        self._plugins[name] = plugin_class

    def get(self, name: str, config: Optional[Any] = None) -> T:
        """
        플러그인 인스턴스 조회 (싱글톤)

        Args:
            name: 플러그인 이름
            config: 초기화 설정

        Returns:
            플러그인 인스턴스
        """
        if name not in self._plugins:
            available = ", ".join(self._plugins.keys())
            raise KeyError(f"플러그인 '{name}' 없음. 사용 가능: {available}")

        # 싱글톤 패턴 - 이미 생성된 인스턴스가 있으면 재사용
        if name not in self._instances:
            instance = self._plugins[name]()
            instance.initialize(config)
            self._instances[name] = instance

        return self._instances[name]

    def create(self, name: str, config: Optional[Any] = None) -> T:
        """
        새 플러그인 인스턴스 생성 (매번 새로 생성)

        Args:
            name: 플러그인 이름
            config: 초기화 설정

        Returns:
            새 플러그인 인스턴스
        """
        if name not in self._plugins:
            available = ", ".join(self._plugins.keys())
            raise KeyError(f"플러그인 '{name}' 없음. 사용 가능: {available}")

        instance = self._plugins[name]()
        instance.initialize(config)
        return instance

    def list_available(self) -> list[str]:
        """등록된 플러그인 이름 목록"""
        return list(self._plugins.keys())

    def shutdown_all(self) -> None:
        """모든 활성 인스턴스 종료"""
        for instance in self._instances.values():
            instance.shutdown()
        self._instances.clear()
