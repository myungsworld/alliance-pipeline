# Makefile - Alliance Pipeline 명령어 모음

.PHONY: help build up down logs shell test scrape pipeline clean

# 기본 명령어 (make만 치면 help 출력)
help:
	@echo "Alliance Pipeline 명령어"
	@echo ""
	@echo "Docker:"
	@echo "  make build     - Docker 이미지 빌드"
	@echo "  make up        - 컨테이너 시작"
	@echo "  make down      - 컨테이너 중지"
	@echo "  make logs      - 로그 보기"
	@echo "  make shell     - 컨테이너 쉘 접속"
	@echo ""
	@echo "실행:"
	@echo "  make scrape    - 쿠팡 할인 크롤링 테스트"
	@echo "  make pipeline  - 파이프라인 실행"
	@echo "  make server    - API 서버 실행"
	@echo "  make list      - 등록된 플러그인 목록"
	@echo ""
	@echo "개발:"
	@echo "  make test      - 테스트 실행"
	@echo "  make clean     - 캐시/임시파일 삭제"

# === Docker ===

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f app

shell:
	docker-compose exec app /bin/bash

restart: down up

# === 실행 ===

scrape:
	docker-compose exec -T app python scripts/run.py scrape coupang.deals --max 5

scrape-keyword:
	@read -p "키워드: " keyword; \
	docker-compose exec -T app python scripts/run.py scrape coupang.products --keyword "$$keyword" --max 10

pipeline:
	docker-compose exec -T app python scripts/run.py pipeline coupang-to-blog

server:
	docker-compose exec -T app python scripts/run.py server --port 8000

list:
	docker-compose exec -T app python scripts/run.py list scrapers
	docker-compose exec -T app python scripts/run.py list publishers
	docker-compose exec -T app python scripts/run.py list actions

# === 개발 ===

test:
	docker-compose exec app pytest tests/ -v

lint:
	docker-compose exec app ruff check src/

format:
	docker-compose exec app black src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache 2>/dev/null || true

# === 초기 설정 ===

init:
	@if [ ! -f config/secrets.yaml ]; then \
		cp config/secrets.yaml.example config/secrets.yaml; \
		echo "config/secrets.yaml 생성됨 - API 키를 입력하세요"; \
	else \
		echo "config/secrets.yaml 이미 존재함"; \
	fi
