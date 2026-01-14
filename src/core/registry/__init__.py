# registry/ - 플러그인 레지스트리
# 어댑터 패턴의 핵심 - 구현체를 동적으로 등록하고 조회

from .plugin import Plugin, PluginRegistry

__all__ = ["Plugin", "PluginRegistry"]
