# AI 숏폼 자동화 파이프라인 개발 문서

## 프로젝트 개요
물건(objects)과 생명체(creatures)의 랜덤 조합을 기반으로 AI가 재미있는 숏폼 스크립트를 생성하고, 텔레그램으로 승인/재시도를 관리하는 자동화 파이프라인

## 현재 진행 상황

### ✅ 완료된 작업

1. **Docker 환경 구성**
   - n8n 컨테이너 (포트 5678)
   - PostgreSQL 컨테이너 (포트 5432)
   - 볼륨 마운트: `n8n_data`, `postgres_data`, `./files`, `./workflows`

2. **데이터베이스 설계**
   - `objects` 테이블: 물건 데이터 (251개 항목, 20개 카테고리)
   - `creatures` 테이블: 생명체 데이터 (231개 항목, 15개 카테고리)
   - `combinations_used` 테이블: 사용된 조합 기록
   - `random_unused_combination` 뷰: 미사용 랜덤 조합 조회

3. **ngrok HTTPS 터널 설정**
   - ngrok 설치 완료
   - WEBHOOK_URL 환경변수 설정
   - Docker 컨테이너에 WEBHOOK_URL 적용 완료

4. **텔레그램 봇 설정**
   - 봇 이름: @your_bot_name
   - Chat ID: .env 파일 참조
   - 메시지 전송 정상 작동 확인

5. **워크플로우 1: llmFlow (조합 선택)**
   - Telegram Trigger (On Message) 설정
   - IF 노드로 /start 명령어 필터링
   - PostgreSQL: 5개 랜덤 조합 조회
   - Code 노드: 인라인 키보드 버튼 생성
   - HTTP Request: Telegram API로 5개 버튼 전송 완료

6. **워크플로우 백업 시스템 구축**
   - docker-compose.yaml에 `./workflows:/workflows` 볼륨 마운트 추가
   - n8n CLI로 워크플로우 JSON 내보내기 설정
   - n8n REST API로 워크플로우 삭제 기능 구현
   - 불필요한 아카이브 워크플로우 정리 완료

7. **문서화**
   - README.md: 다른 컴퓨터에서 환경 설정 가이드 추가
   - DEVELOPMENT.md: 개발 일지 및 워크플로우 관리 방법 문서화

### 🔄 진행 중

8. **워크플로우 2: Callback Handler (버튼 클릭 처리)**
   - Telegram Trigger (Callback Query) 설정
   - IF 노드로 callback_data 분기 처리 구현 중
     - `select_*` → 조합 선택 → LLM 실행
     - `approve` → DB 저장 → 완료 메시지
     - `retry` → LLM 재실행

### ⏳ 예정된 작업

9. **LLM Chain 연동** (조합 선택 후 스크립트 생성)
10. **승인 시 combinations_used 테이블에 저장**
11. **워크플로우 활성화 및 통합 테스트**
12. **영상 생성 연동** (추후)

---

## 기술 스택

| 구성요소 | 기술 |
|---------|------|
| 워크플로우 자동화 | n8n (self-hosted) |
| 데이터베이스 | PostgreSQL 16 |
| AI 모델 | Google Gemini (gemini-2.5-flash) |
| 메시지/알림 | Telegram Bot API |
| 터널링 | ngrok |
| 컨테이너 | Docker Compose |

---

## 워크플로우 구조

### 워크플로우 1: llmFlow (조합 선택)
```
[Telegram Trigger: On Message]
    ↓
[IF: message.text == "/start"]
    ↓ (true)
[PostgreSQL: 5개 랜덤 조합 조회]
    ↓
[Code: 인라인 키보드 버튼 생성]
    ↓
[HTTP Request: Telegram API sendMessage]
    → 5개 조합 버튼 전송
```

### 워크플로우 2: Callback Handler (버튼 클릭 처리)
```
[Telegram Trigger: Callback Query]
    ↓
[IF: callback_data.startsWith("select_")]
    ↓
[true] → Code (파싱) → LLM Chain → Telegram (스크립트 + 승인/재생성 버튼)
[false] →
    [IF: callback_data == "approve"]
        [true] → PostgreSQL (INSERT) → Telegram (완료 메시지)
        [false] → LLM Chain (재실행) → Telegram (새 스크립트)
```

---

## 환경 변수 (.env)

```bash
# PostgreSQL
POSTGRES_USER=n8n
POSTGRES_PASSWORD=****
POSTGRES_DB=content_db

# Timezone
TZ=Asia/Seoul

# API Keys
GEMINI_API_KEY=****

# Telegram
TELEGRAM_BOT_TOKEN=****
TELEGRAM_CHAT_ID=****

# ngrok
NGROK_AUTHTOKEN=****
WEBHOOK_URL=https://your-ngrok-url.ngrok-free.dev

# n8n API (워크플로우 관리용)
N8N_API_KEY=****
```

---

## n8n 워크플로우 백업/복원

### CLI로 전체 워크플로우 내보내기 (권장)
```bash
# 모든 워크플로우를 workflows/ 폴더에 JSON으로 내보내기
docker exec n8n n8n export:workflow --backup --output=/workflows/
```

- `--backup`: 각 워크플로우를 별도 JSON 파일로 저장 (보기 좋게 포맷팅)
- `--output=/workflows/`: 저장 경로 (docker-compose에서 `./workflows`와 연결됨)
- 결과: `workflows/` 폴더에 워크플로우별 JSON 파일 생성
- 이 파일들을 git에 커밋하면 다른 컴퓨터에서 동일한 환경 구성 가능

### UI에서 개별 내보내기
1. n8n UI에서 워크플로우 열기
2. 우측 상단 `...` 메뉴 클릭
3. `Download` 선택 → JSON 파일 저장

### 워크플로우 가져오기
1. n8n UI에서 `Import from File` 클릭
2. `workflows/` 폴더의 JSON 파일 선택
3. Credential 재설정 필요:
   - PostgreSQL (Host: `postgres`, DB: `content_db`)
   - Telegram Bot Token
   - Google Gemini API Key

### 워크플로우 삭제

**1. workflows 폴더에서 JSON 삭제:**
```bash
rm workflows/워크플로우ID.json
```

**2. n8n API로 워크플로우 완전 삭제:**
```bash
# API 키는 n8n UI > Settings > API에서 생성
curl -X DELETE "http://localhost:5678/api/v1/workflows/워크플로우ID" \
  -H "X-N8N-API-KEY: your_api_key"
```

**3. (대안) n8n UI에서 삭제:**
1. http://localhost:5678 접속
2. Workflows 메뉴 → 필터에서 "Archived" 선택
3. 워크플로우 `...` → Delete 클릭

### Docker 볼륨 백업 (전체 데이터)
```bash
# n8n 데이터 백업
docker run --rm -v alliance-pipeline_n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n_backup.tar.gz /data

# 복원
docker run --rm -v alliance-pipeline_n8n_data:/data -v $(pwd):/backup alpine tar xzf /backup/n8n_backup.tar.gz -C /
```

---

## 변경 이력

| 날짜 | 작업 내용 |
|------|----------|
| 2025-01-25 | 프로젝트 초기 설정, Docker 환경 구성 |
| 2025-01-25 | 데이터베이스 스키마 및 시드 데이터 통합 |
| 2025-01-25 | n8n + PostgreSQL + Gemini 연동 완료 |
| 2025-01-25 | 텔레그램 봇 메시지 전송 테스트 완료 |
| 2025-01-25 | ngrok 설치 및 WEBHOOK_URL 설정 완료 |
| 2025-01-25 | Telegram Trigger (Callback Query) 설정 완료 |
| 2025-01-25 | 워크플로우 1 완성: /start → 5개 조합 버튼 전송 |
| 2025-01-25 | 워크플로우 2 진행 중: Callback Query 분기 처리 |
| 2025-01-25 | 워크플로우 백업 시스템 구축: CLI 내보내기 + workflows/ 폴더 연동 |
| 2025-01-25 | n8n API 연동: 워크플로우 삭제 기능 구현 |
| 2025-01-25 | 불필요한 워크플로우 정리 (button handler, My workflow 2 등 삭제) |
| 2025-01-25 | README.md 업데이트: 다른 컴퓨터 환경 설정 가이드 추가 |
