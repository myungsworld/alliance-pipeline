# client.py - 티스토리 API 클라이언트
# 티스토리 Open API를 통한 글 발행

from typing import Optional, Any
import httpx

from src.publishers.base import Publisher, Content, PublishResult, PublisherRegistry


class TistoryPublisher(Publisher):
    """
    티스토리 발행 채널

    티스토리 Open API를 사용하여 블로그 글 발행
    공식 API 사용으로 안전한 자동화

    사전 준비:
    1. https://www.tistory.com/guide/api/manage/register 에서 앱 등록
    2. access_token 발급

    사용법:
        publisher = TistoryPublisher(
            access_token="토큰",
            blog_name="myblog"
        )
        content = Content(title="제목", body="내용")
        result = await publisher.publish(content)
    """

    API_BASE = "https://www.tistory.com/apis"

    def __init__(
        self,
        access_token: str,
        blog_name: str,
        category_id: Optional[str] = None,
        visibility: int = 3  # 0: 비공개, 1: 보호, 3: 발행
    ):
        self._access_token = access_token
        self._blog_name = blog_name
        self._category_id = category_id
        self._visibility = visibility

    @property
    def name(self) -> str:
        return "tistory"

    def initialize(self, config: Optional[Any] = None) -> None:
        """설정에서 초기화"""
        if config:
            self._access_token = config.get("access_token", self._access_token)
            self._blog_name = config.get("blog_name", self._blog_name)
            self._category_id = config.get("category_id", self._category_id)

    async def publish(self, content: Content) -> PublishResult:
        """글 발행"""
        try:
            # HTML 형식으로 본문 변환
            html_body = self._convert_to_html(content.body)

            # API 요청 데이터
            data = {
                "access_token": self._access_token,
                "output": "json",
                "blogName": self._blog_name,
                "title": content.title,
                "content": html_body,
                "visibility": str(self._visibility),
            }

            # 카테고리 설정
            if self._category_id:
                data["category"] = self._category_id

            # 태그 추가
            if content.tags:
                data["tag"] = ",".join(content.tags)

            # API 호출
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.API_BASE}/post/write",
                    data=data,
                    timeout=30
                )
                response.raise_for_status()

            result = response.json()

            if result.get("tistory", {}).get("status") == "200":
                post_id = result["tistory"].get("postId")
                url = result["tistory"].get("url")
                return PublishResult.ok(url=url, post_id=post_id)
            else:
                error_msg = result.get("tistory", {}).get("error_message", "알 수 없는 오류")
                return PublishResult.fail(error_msg)

        except httpx.HTTPStatusError as e:
            return PublishResult.fail(f"HTTP 오류: {e.response.status_code}")
        except Exception as e:
            return PublishResult.fail(f"발행 에러: {str(e)}")

    def _convert_to_html(self, text: str) -> str:
        """
        텍스트를 HTML로 변환

        간단한 마크다운 형식 지원
        """
        # 줄바꿈 처리
        html = text.replace("\n\n", "</p><p>").replace("\n", "<br>")
        html = f"<p>{html}</p>"

        # 간단한 마크다운 변환
        import re

        # **bold** -> <strong>bold</strong>
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)

        # *italic* -> <em>italic</em>
        html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

        # [text](url) -> <a href="url">text</a>
        html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)

        return html

    async def get_categories(self) -> list:
        """카테고리 목록 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.API_BASE}/category/list",
                params={
                    "access_token": self._access_token,
                    "output": "json",
                    "blogName": self._blog_name
                }
            )
            response.raise_for_status()

        result = response.json()
        categories = result.get("tistory", {}).get("item", {}).get("categories", [])
        return categories

    async def get_blog_info(self) -> dict:
        """블로그 정보 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.API_BASE}/blog/info",
                params={
                    "access_token": self._access_token,
                    "output": "json"
                }
            )
            response.raise_for_status()

        result = response.json()
        return result.get("tistory", {}).get("item", {})


# 레지스트리에 등록
PublisherRegistry.register_with_name("tistory", TistoryPublisher)
