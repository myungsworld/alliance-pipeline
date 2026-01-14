# bot.py - 텔레그램 봇 클라이언트
# 텔레그램 Bot API를 통한 채널 메시지 발송

from typing import Optional, Any
import httpx

from src.publishers.base import Publisher, Content, PublishResult, PublisherRegistry


class TelegramPublisher(Publisher):
    """
    텔레그램 발행 채널

    텔레그램 Bot API를 사용하여 채널에 메시지 발송
    완전 무료 + 자동화 친화적

    사전 준비:
    1. @BotFather로 봇 생성하여 토큰 발급
    2. 봇을 채널에 관리자로 추가

    사용법:
        publisher = TelegramPublisher(
            bot_token="123456:ABC...",
            chat_id="@mychannel"  # 또는 -100123456789
        )
        content = Content(title="제목", body="내용")
        result = await publisher.publish(content)
    """

    API_BASE = "https://api.telegram.org"

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        parse_mode: str = "HTML"  # HTML, Markdown, MarkdownV2
    ):
        self._bot_token = bot_token
        self._chat_id = chat_id
        self._parse_mode = parse_mode

    @property
    def name(self) -> str:
        return "telegram"

    @property
    def api_url(self) -> str:
        return f"{self.API_BASE}/bot{self._bot_token}"

    def initialize(self, config: Optional[Any] = None) -> None:
        """설정에서 초기화"""
        if config:
            self._bot_token = config.get("bot_token", self._bot_token)
            self._chat_id = config.get("chat_id", self._chat_id)

    async def publish(self, content: Content) -> PublishResult:
        """메시지 발송"""
        try:
            # 메시지 포맷팅
            message = self._format_message(content)

            # 이미지가 있으면 사진과 함께 발송
            if content.images:
                return await self._send_photo(message, content.images[0])

            # 텍스트만 발송
            return await self._send_message(message)

        except Exception as e:
            return PublishResult.fail(f"발송 에러: {str(e)}")

    async def _send_message(self, text: str) -> PublishResult:
        """텍스트 메시지 발송"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self._chat_id,
                    "text": text,
                    "parse_mode": self._parse_mode,
                    "disable_web_page_preview": False
                },
                timeout=30
            )
            response.raise_for_status()

        result = response.json()

        if result.get("ok"):
            message_id = result["result"]["message_id"]
            return PublishResult.ok(post_id=str(message_id))
        else:
            return PublishResult.fail(result.get("description", "알 수 없는 오류"))

    async def _send_photo(self, caption: str, photo_url: str) -> PublishResult:
        """사진과 함께 메시지 발송"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/sendPhoto",
                json={
                    "chat_id": self._chat_id,
                    "photo": photo_url,
                    "caption": caption[:1024],  # 캡션 길이 제한
                    "parse_mode": self._parse_mode
                },
                timeout=30
            )
            response.raise_for_status()

        result = response.json()

        if result.get("ok"):
            message_id = result["result"]["message_id"]
            return PublishResult.ok(post_id=str(message_id))
        else:
            return PublishResult.fail(result.get("description", "알 수 없는 오류"))

    def _format_message(self, content: Content) -> str:
        """콘텐츠를 텔레그램 메시지 형식으로 변환"""
        if self._parse_mode == "HTML":
            return self._format_html(content)
        else:
            return self._format_plain(content)

    def _format_html(self, content: Content) -> str:
        """HTML 형식으로 포맷팅"""
        parts = []

        # 제목
        parts.append(f"<b>{content.title}</b>")

        # 본문
        parts.append("")
        parts.append(content.body)

        # 태그
        if content.tags:
            tags_str = " ".join(f"#{tag}" for tag in content.tags)
            parts.append("")
            parts.append(tags_str)

        return "\n".join(parts)

    def _format_plain(self, content: Content) -> str:
        """일반 텍스트 형식으로 포맷팅"""
        parts = [content.title, "", content.body]

        if content.tags:
            parts.append("")
            parts.append(" ".join(f"#{tag}" for tag in content.tags))

        return "\n".join(parts)

    async def get_me(self) -> dict:
        """봇 정보 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/getMe")
            response.raise_for_status()
        return response.json().get("result", {})

    async def get_chat(self) -> dict:
        """채널 정보 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/getChat",
                params={"chat_id": self._chat_id}
            )
            response.raise_for_status()
        return response.json().get("result", {})


# 레지스트리에 등록
PublisherRegistry.register_with_name("telegram", TelegramPublisher)
