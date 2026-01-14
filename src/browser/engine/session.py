# session.py - 브라우저 세션 관리
# 로그인 상태, 쿠키 등 세션 정보 관리

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


class BrowserSession:
    """
    브라우저 세션 관리

    쿠키, 로컬 스토리지 등 세션 정보를 저장/복원
    로그인 상태 유지에 사용

    사용 예시:
        session = BrowserSession("naver")
        session.load(browser)  # 저장된 세션 복원
        # ... 로그인 작업 ...
        session.save(browser)  # 세션 저장
    """

    def __init__(self, name: str, storage_path: str = "./data/sessions"):
        self._name = name
        self._storage_path = Path(storage_path)
        self._storage_path.mkdir(parents=True, exist_ok=True)

    @property
    def session_file(self) -> Path:
        """세션 파일 경로"""
        return self._storage_path / f"{self._name}.json"

    def save(self, browser) -> None:
        """
        현재 브라우저 세션 저장

        쿠키 + 로컬 스토리지 저장
        """
        driver = browser.driver

        session_data = {
            "name": self._name,
            "saved_at": datetime.now().isoformat(),
            "url": driver.current_url,
            "cookies": driver.get_cookies(),
            "local_storage": self._get_local_storage(driver),
        }

        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

    def load(self, browser) -> bool:
        """
        저장된 세션 복원

        Returns:
            성공 여부
        """
        if not self.session_file.exists():
            return False

        try:
            with open(self.session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            driver = browser.driver

            # 쿠키 복원 (같은 도메인에서만 가능)
            for cookie in session_data.get("cookies", []):
                try:
                    driver.add_cookie(cookie)
                except Exception:
                    pass  # 도메인 불일치 등으로 실패할 수 있음

            # 로컬 스토리지 복원
            local_storage = session_data.get("local_storage", {})
            self._set_local_storage(driver, local_storage)

            return True

        except Exception as e:
            print(f"세션 로드 실패 [{self._name}]: {e}")
            return False

    def delete(self) -> None:
        """세션 삭제"""
        if self.session_file.exists():
            self.session_file.unlink()

    def exists(self) -> bool:
        """세션 존재 여부"""
        return self.session_file.exists()

    def _get_local_storage(self, driver) -> Dict[str, str]:
        """로컬 스토리지 가져오기"""
        try:
            return driver.execute_script(
                "return Object.fromEntries(Object.entries(localStorage));"
            )
        except Exception:
            return {}

    def _set_local_storage(self, driver, data: Dict[str, str]) -> None:
        """로컬 스토리지 설정"""
        for key, value in data.items():
            try:
                driver.execute_script(
                    f"localStorage.setItem('{key}', '{value}');"
                )
            except Exception:
                pass
