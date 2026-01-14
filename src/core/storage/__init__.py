# storage/ - 저장소 어댑터
# 어댑터 패턴으로 다양한 저장소 구현체 교체 가능
# file, sqlite, mysql, mongodb, redis 등

from .base import Storage, StorageRegistry
from .file import FileStorage

__all__ = ["Storage", "StorageRegistry", "FileStorage"]
