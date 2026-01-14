# base.py - 저장소 인터페이스
# 어댑터 패턴: 이 인터페이스만 구현하면 어떤 DB든 교체 가능

from abc import abstractmethod
from typing import Any, Dict, List, Optional

from ..registry.plugin import Plugin, PluginRegistry


class Storage(Plugin):
    """
    저장소 인터페이스 (어댑터 패턴)

    구현체 예시:
    - FileStorage: JSON 파일 기반
    - SQLiteStorage: SQLite DB
    - MySQLStorage: MySQL DB
    - MongoDBStorage: MongoDB
    - RedisStorage: Redis

    사용법:
        storage = StorageRegistry.get("mysql")
        storage.save("products", {"id": 1, "name": "상품"})
        product = storage.get("products", "1")
    """

    @abstractmethod
    def save(self, collection: str, data: Dict[str, Any], key: Optional[str] = None) -> str:
        """
        데이터 저장

        Args:
            collection: 컬렉션/테이블 이름
            data: 저장할 데이터
            key: 키 (없으면 자동 생성)

        Returns:
            저장된 데이터의 키
        """
        pass

    @abstractmethod
    def get(self, collection: str, key: str) -> Optional[Dict[str, Any]]:
        """
        데이터 조회

        Args:
            collection: 컬렉션/테이블 이름
            key: 조회할 키

        Returns:
            데이터 (없으면 None)
        """
        pass

    @abstractmethod
    def find(
        self,
        collection: str,
        query: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        데이터 검색

        Args:
            collection: 컬렉션/테이블 이름
            query: 검색 조건 (필드: 값)
            limit: 최대 결과 수

        Returns:
            매칭되는 데이터 리스트
        """
        pass

    @abstractmethod
    def update(self, collection: str, key: str, data: Dict[str, Any]) -> bool:
        """
        데이터 업데이트

        Args:
            collection: 컬렉션/테이블 이름
            key: 업데이트할 키
            data: 업데이트할 데이터

        Returns:
            성공 여부
        """
        pass

    @abstractmethod
    def delete(self, collection: str, key: str) -> bool:
        """
        데이터 삭제

        Args:
            collection: 컬렉션/테이블 이름
            key: 삭제할 키

        Returns:
            성공 여부
        """
        pass

    @abstractmethod
    def exists(self, collection: str, key: str) -> bool:
        """데이터 존재 여부 확인"""
        pass


# 저장소 레지스트리 (싱글톤)
StorageRegistry: PluginRegistry[Storage] = PluginRegistry()
