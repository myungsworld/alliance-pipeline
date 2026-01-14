# file.py - 파일 기반 저장소
# JSON 파일로 데이터 저장 (개발/테스트용)

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import Storage, StorageRegistry


class FileStorage(Storage):
    """
    파일 기반 저장소 구현체

    각 컬렉션이 하나의 JSON 파일로 저장됨
    간단한 개발/테스트 용도로 적합

    예시:
        storage = FileStorage()
        storage.initialize({"path": "./data"})
        storage.save("products", {"name": "상품1"})
    """

    def __init__(self):
        self._base_path: Path = Path("./data")

    @property
    def name(self) -> str:
        return "file"

    def initialize(self, config: Optional[Any] = None) -> None:
        """저장소 초기화 - 경로 설정 및 디렉토리 생성"""
        if config and hasattr(config, "path"):
            self._base_path = Path(config.path)
        elif config and isinstance(config, dict):
            self._base_path = Path(config.get("path", "./data"))

        self._base_path.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, collection: str) -> Path:
        """컬렉션의 파일 경로"""
        return self._base_path / f"{collection}.json"

    def _load_collection(self, collection: str) -> Dict[str, Any]:
        """컬렉션 데이터 로드"""
        filepath = self._get_file_path(collection)
        if not filepath.exists():
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_collection(self, collection: str, data: Dict[str, Any]) -> None:
        """컬렉션 데이터 저장"""
        filepath = self._get_file_path(collection)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save(self, collection: str, data: Dict[str, Any], key: Optional[str] = None) -> str:
        """데이터 저장"""
        key = key or str(uuid.uuid4())
        collection_data = self._load_collection(collection)
        collection_data[key] = data
        self._save_collection(collection, collection_data)
        return key

    def get(self, collection: str, key: str) -> Optional[Dict[str, Any]]:
        """데이터 조회"""
        collection_data = self._load_collection(collection)
        return collection_data.get(key)

    def find(
        self,
        collection: str,
        query: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """데이터 검색"""
        collection_data = self._load_collection(collection)
        results = []

        for key, item in collection_data.items():
            # 쿼리가 없으면 전체 반환
            if query is None:
                results.append({"_key": key, **item})
                continue

            # 쿼리 조건 매칭
            match = all(item.get(k) == v for k, v in query.items())
            if match:
                results.append({"_key": key, **item})

            # limit 체크
            if limit and len(results) >= limit:
                break

        return results

    def update(self, collection: str, key: str, data: Dict[str, Any]) -> bool:
        """데이터 업데이트"""
        collection_data = self._load_collection(collection)
        if key not in collection_data:
            return False

        collection_data[key].update(data)
        self._save_collection(collection, collection_data)
        return True

    def delete(self, collection: str, key: str) -> bool:
        """데이터 삭제"""
        collection_data = self._load_collection(collection)
        if key not in collection_data:
            return False

        del collection_data[key]
        self._save_collection(collection, collection_data)
        return True

    def exists(self, collection: str, key: str) -> bool:
        """데이터 존재 여부"""
        collection_data = self._load_collection(collection)
        return key in collection_data


# 레지스트리에 등록
StorageRegistry.register_with_name("file", FileStorage)
