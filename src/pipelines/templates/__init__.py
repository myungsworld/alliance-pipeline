# templates/ - 미리 정의된 파이프라인 템플릿
# 자주 사용되는 파이프라인 조합

from .coupang_to_blog import create_coupang_to_blog_pipeline

__all__ = ["create_coupang_to_blog_pipeline"]
