# actions/ - 브라우저 액션 플러그인
# 각 사이트별 자동화 액션 (로그인, 글쓰기 등)

from .base import Action, ActionResult, ActionRegistry

__all__ = ["Action", "ActionResult", "ActionRegistry"]
