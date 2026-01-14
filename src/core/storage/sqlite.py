# sqlite.py - SQLite 저장소
# 경량 관계형 DB (서버 필요 없음)

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import Storage, StorageRegistry


class SQLiteStorage(Storage):
    """
    SQLite 저장소 구현체

    서버 없이 파일 하나로 관계형 DB 사용 가능
    FileStorage보다 성능 좋고, 동시성 지원

    예시:
        storage = SQLiteStorage()
        storage.initialize({"path": "./data/db.sqlite"})
    """

    def __init__(self):
        self._db_path: Path = Path("./data/db.sqlite")
        self._conn: Optional[sqlite3.Connection] = None

    @property
    def name(self) -> str:
        return "sqlite"

    def initialize(self, config: Optional[Any] = None) -> None:
        """DB 연결 초기화"""
        if config and hasattr(config, "path"):
            self._db_path = Path(config.path)
        elif config and isinstance(config, dict):
            self._db_path = Path(config.get("path", "./data/db.sqlite"))

        # 디렉토리 생성
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        # DB 연결
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

    def shutdown(self) -> None:
        """DB 연결 종료"""
        if self._conn:
            self._conn.close()
            self._conn = None

    def _ensure_table(self, collection: str) -> None:
        """테이블이 없으면 생성"""
        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {collection} (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def save(self, collection: str, data: Dict[str, Any], key: Optional[str] = None) -> str:
        """데이터 저장"""
        self._ensure_table(collection)
        key = key or str(uuid.uuid4())

        self._conn.execute(
            f"INSERT OR REPLACE INTO {collection} (key, data) VALUES (?, ?)",
            (key, json.dumps(data, ensure_ascii=False))
        )
        self._conn.commit()
        return key

    def get(self, collection: str, key: str) -> Optional[Dict[str, Any]]:
        """데이터 조회"""
        self._ensure_table(collection)

        cursor = self._conn.execute(
            f"SELECT data FROM {collection} WHERE key = ?",
            (key,)
        )
        row = cursor.fetchone()
        return json.loads(row["data"]) if row else None

    def find(
        self,
        collection: str,
        query: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """데이터 검색 (간단한 JSON 필드 매칭)"""
        self._ensure_table(collection)

        sql = f"SELECT key, data FROM {collection}"
        if limit:
            sql += f" LIMIT {limit}"

        cursor = self._conn.execute(sql)
        results = []

        for row in cursor:
            item = json.loads(row["data"])
            item["_key"] = row["key"]

            # 쿼리 필터링
            if query is None:
                results.append(item)
            elif all(item.get(k) == v for k, v in query.items()):
                results.append(item)

        return results

    def update(self, collection: str, key: str, data: Dict[str, Any]) -> bool:
        """데이터 업데이트"""
        existing = self.get(collection, key)
        if not existing:
            return False

        existing.update(data)
        self.save(collection, existing, key)
        return True

    def delete(self, collection: str, key: str) -> bool:
        """데이터 삭제"""
        self._ensure_table(collection)

        cursor = self._conn.execute(
            f"DELETE FROM {collection} WHERE key = ?",
            (key,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def exists(self, collection: str, key: str) -> bool:
        """데이터 존재 여부"""
        self._ensure_table(collection)

        cursor = self._conn.execute(
            f"SELECT 1 FROM {collection} WHERE key = ?",
            (key,)
        )
        return cursor.fetchone() is not None


# 레지스트리에 등록
StorageRegistry.register_with_name("sqlite", SQLiteStorage)
