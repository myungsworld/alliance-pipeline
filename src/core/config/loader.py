# loader.py - 설정 로더
# 다양한 소스(yaml, env, json)에서 설정을 로드하고 병합

import os
from pathlib import Path
from typing import Optional, Dict, Any

import yaml
from dotenv import load_dotenv

from ..exceptions import ConfigError
from .schema import Config


class ConfigLoader:
    """
    설정 로더 - 여러 소스에서 설정을 로드하고 병합

    우선순위: 환경변수 > secrets.yaml > {env}.yaml > default.yaml
    """

    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        self._config: Optional[Config] = None

    def load(self, env: Optional[str] = None) -> Config:
        """
        설정 로드

        Args:
            env: 환경 이름 (development, production 등)
                 지정하지 않으면 ENV 환경변수 사용

        Returns:
            병합된 Config 객체
        """
        # .env 파일 로드
        load_dotenv()

        env = env or os.getenv("ENV", "development")

        # 설정 파일들 병합
        merged: Dict[str, Any] = {}

        # 1. default.yaml 로드
        merged = self._merge(merged, self._load_yaml("default.yaml"))

        # 2. {env}.yaml 로드
        merged = self._merge(merged, self._load_yaml(f"{env}.yaml"))

        # 3. secrets.yaml 로드 (존재하면)
        merged = self._merge(merged, self._load_yaml("secrets.yaml"))

        # 4. 환경변수로 오버라이드
        merged = self._apply_env_overrides(merged)

        # 5. env 값 설정
        merged["env"] = env

        try:
            self._config = Config(**merged)
            return self._config
        except Exception as e:
            raise ConfigError(f"설정 검증 실패: {e}")

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """YAML 파일 로드 (없으면 빈 딕셔너리 반환)"""
        filepath = self.config_dir / filename
        if not filepath.exists():
            return {}

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigError(f"YAML 로드 실패 ({filename}): {e}")

    def _merge(self, base: Dict, override: Dict) -> Dict:
        """딕셔너리 깊은 병합"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge(result[key], value)
            else:
                result[key] = value
        return result

    def _apply_env_overrides(self, config: Dict) -> Dict:
        """
        환경변수로 설정 오버라이드

        예: BROWSER_HEADLESS=true -> config["browser"]["headless"] = True
        """
        env_mappings = {
            "BROWSER_HEADLESS": ("browser", "headless", lambda x: x.lower() == "true"),
            "BROWSER_TIMEOUT": ("browser", "timeout", int),
            "STORAGE_TYPE": ("storage", "type", str),
            "QUEUE_TYPE": ("queue", "type", str),
            "SERVER_PORT": ("server", "port", int),
            "DEBUG": ("debug", None, lambda x: x.lower() == "true"),
        }

        for env_key, (section, key, converter) in env_mappings.items():
            value = os.getenv(env_key)
            if value is not None:
                if key is None:
                    config[section] = converter(value)
                else:
                    if section not in config:
                        config[section] = {}
                    config[section][key] = converter(value)

        return config

    @property
    def config(self) -> Config:
        """로드된 설정 반환 (로드 안됐으면 자동 로드)"""
        if self._config is None:
            self.load()
        return self._config
