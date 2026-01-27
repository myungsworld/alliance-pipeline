# AI 숏폼 자동화 파이프라인

n8n + Telegram + Google Gemini를 활용한 AI 숏폼 콘텐츠 자동 생성 시스템

## 컨셉

**랜덤 물건 + 랜덤 생명체** 조합으로 예측 불가능한 재미있는 숏폼 콘텐츠 자동 생성

### 두 가지 컨텐츠 모드

| 모드 | 설명 | 예시 |
|------|------|------|
| **조우** | 생명체가 물건을 마주했을 때 벌어지는 상황 | 펭귄 + 우산 → 5가지 웃긴 상황 |
| **대결** | 두 조합이 맞붙는 시나리오 | 칼 든 치킨 vs 방패 든 고양이 |

## 기술 스택

| 구성요소 | 기술 |
|----------|------|
| 워크플로우 자동화 | n8n (self-hosted) |
| 데이터베이스 | PostgreSQL 16 |
| LLM | Google Gemini |
| 메신저 봇 | Telegram Bot API |
| 터널링 | ngrok (Webhook용) |
| 컨테이너 | Docker Compose |

## 워크플로우 구조

### 1. start - 시작 워크플로우
텔레그램 메시지 트리거로 랜덤 조합 버튼 전송

```
[Telegram: "조우" or "대결" 메시지]
    ↓
[Switch: 명령어 분기]
    ├─ "조우" → [PostgreSQL: 10개 랜덤 조합] → [버튼 생성] → [Telegram 전송]
    └─ "대결" → [PostgreSQL: 10개 조합] → [5쌍 vs 버튼 생성] → [Telegram 전송]
```

### 2. write - 콜백 처리 워크플로우
버튼 클릭 시 LLM으로 스크립트 생성

```
[Telegram: Callback Query]
    ↓
[Switch: callback_data 분기]
    │
    ├─ "select_*" (조우)
    │   ↓
    │   [Parse: object_id, creature_id 추출]
    │   ↓
    │   [PostgreSQL: 이름 조회]
    │   ↓
    │   [Gemini LLM: 5가지 상황 생성]
    │   ↓
    │   [PostgreSQL: encounter_scripts INSERT]
    │   ↓
    │   [Telegram: 결과 + 버튼 전송]
    │
    └─ "vs_*" (대결)
        ↓
        [Parse: 4개 ID 추출]
        ↓
        [PostgreSQL: 양팀 이름 조회]
        ↓
        [Gemini LLM: 대결 시나리오 생성]
        ↓
        [Telegram: 결과 전송]
```

### 3. My workflow - 이미지 생성 처리
"이미지 생성" 버튼 클릭 시 저장된 스크립트 조회

```
[Telegram: "encounter_*" Callback]
    ↓
[Switch: encounter_ 분기]
    ↓
[PostgreSQL: encounter_scripts 조회 by ID]
    ↓
[이미지 생성 API 연동 예정]
```

## 데이터베이스 구조

### 테이블

```sql
-- 물건 (251개, 20개 카테고리)
objects (id, name, category, created_at)

-- 생명체 (231개, 15개 카테고리)
creatures (id, name, category, created_at)

-- 사용된 조합 기록
combinations_used (id, object_id, creature_id, content_type, used_at)

-- LLM 생성 스크립트 저장
encounter_scripts (
    id, object_id, creature_id,
    object_name, creature_name,
    situations JSONB,  -- 5개 상황 배열
    selected_index, status,
    created_at, updated_at
)
```

### 카테고리

**물건 (20개)**
도구, 가전, 탈것, 악기, 무기, 일상용품, 가구, 스포츠, 음식, 건물, 자연물, SF, 판타지, 문구, 장난감, 의료, 주방, 캠핑, 전자기기

**생명체 (15개)**
포유류, 조류, 수중생물, 파충류, 양서류, 곤충, 상상, 직업, 역사, 신화, 공포, 캐릭터, 공룡, 기계, 기타

## 빠른 시작

### 1. 프로젝트 클론
```bash
git clone https://github.com/your-repo/alliance-pipeline.git
cd alliance-pipeline
```

### 2. 환경변수 설정
```bash
cp .env.example .env
```

`.env` 파일 수정:
```bash
# PostgreSQL
POSTGRES_USER=n8n
POSTGRES_PASSWORD=your_password
POSTGRES_DB=content_db

# Timezone
TZ=Asia/Seoul

# API Keys
GEMINI_API_KEY=your_gemini_key
REPLICATE_API_TOKEN=your_replicate_token

# Telegram
TELEGRAM_START_BOT_TOKEN=your_start_bot_token
TELEGRAM_SCRIPT_BOT_TOKEN=your_script_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# ngrok
NGROK_AUTHTOKEN=your_ngrok_token
WEBHOOK_URL=https://your-ngrok-url.ngrok-free.app

# n8n API
N8N_API_KEY=your_n8n_api_key
```

### 3. Docker 실행
```bash
docker compose up -d
```

### 4. Credentials 가져오기
```bash
./scripts/import-credentials.sh
```

### 5. 워크플로우 가져오기
```bash
./scripts/update-workflow.sh
```

### 6. 워크플로우 활성화
n8n API로 활성화하거나 UI에서 토글 ON

## 사용 방법

### 텔레그램에서 실행

1. 봇에게 **"조우"** 메시지 전송 → 10개 랜덤 조합 버튼 표시
2. 원하는 조합 버튼 클릭 → LLM이 5가지 상황 생성
3. **"이미지 생성"** 또는 **"다른 시나리오"** 선택

또는

1. 봇에게 **"대결"** 메시지 전송 → 5개 vs 버튼 표시
2. 원하는 대결 버튼 클릭 → LLM이 대결 시나리오 생성

## 파일 구조

```
alliance-pipeline/
├── docker-compose.yaml    # Docker 설정 (n8n, postgres, ngrok)
├── .env                   # 환경변수 (git 제외)
├── .env.example           # 환경변수 템플릿
├── init.sql               # DB 스키마 + 시드 데이터
├── workflows/             # n8n 워크플로우 백업 (JSON)
├── credentials/           # n8n credentials (환경변수 참조)
│   └── credentials.json
├── scripts/
│   ├── export-credentials.sh  # credentials 내보내기
│   ├── import-credentials.sh  # credentials 가져오기
│   ├── export-workflow.sh     # 워크플로우 내보내기
│   ├── update-workflow.sh     # 워크플로우 가져오기
│   └── pre-commit.sh          # git pre-commit hook
├── DEVELOPMENT.md         # 개발 일지
└── README.md
```

## 멀티 PC 동기화 워크플로우

### Git Pre-commit Hook 설정
```bash
ln -sf ../../scripts/pre-commit.sh .git/hooks/pre-commit
```

### 작업 흐름

**로컬에서 작업 후 커밋:**
1. n8n UI에서 워크플로우/credentials 수정
2. `git commit` 실행 → pre-commit hook이 자동으로:
   - credentials 내보내기
   - workflows 내보내기
3. `git push`

**다른 PC에서 동기화:**
1. `git pull`
2. `docker compose up -d`
3. `./scripts/import-credentials.sh`
4. `./scripts/update-workflow.sh`

### 수동 관리

**Credentials 내보내기:**
```bash
./scripts/export-credentials.sh
```

**Credentials 가져오기:**
```bash
./scripts/import-credentials.sh
```

**워크플로우 내보내기:**
```bash
./scripts/export-workflow.sh
```

**워크플로우 가져오기:**
```bash
./scripts/update-workflow.sh
```

## n8n PostgreSQL 연결 정보

| 필드 | 값 |
|------|------|
| Host | `postgres` |
| Database | `content_db` |
| User | `n8n` |
| Password | `.env` 파일 참조 |
| Port | `5432` |
| SSL | `Disable` |

> Host는 `localhost`가 아닌 `postgres` (Docker 내부 네트워크)

## 접속 URL

| 서비스 | URL |
|--------|-----|
| n8n | http://localhost:5678 |
| ngrok 대시보드 | http://localhost:4040 |
| PostgreSQL | localhost:5432 |

## 진행 상황

### 완료
- [x] Docker 환경 구성 (n8n + PostgreSQL + ngrok)
- [x] DB 스키마 및 시드 데이터 (물건 251개, 생명체 231개)
- [x] Telegram Bot 연동
- [x] ngrok HTTPS 터널 설정
- [x] 워크플로우 1: start (조우/대결 버튼 전송)
- [x] 워크플로우 2: write (LLM 스크립트 생성)
- [x] encounter_scripts 테이블 (LLM 결과 저장)
- [x] 워크플로우 백업 시스템
- [x] 멀티 PC 동기화 (credentials/workflows)
- [x] 환경변수 기반 credentials 관리

### 진행 중
- [ ] 이미지 생성 API 연동 (Replicate SDXL)

### 예정
- [ ] 영상 생성 API 연동 (Runway / Kling)
- [ ] 자동 업로드 (TikTok / YouTube Shorts)
- [ ] 서버 배포 (Oracle Cloud)

## 예상 비용 (콘텐츠 1개당)

| 항목 | 비용 |
|------|------|
| Gemini (스토리) | ~$0.01 |
| Replicate SDXL (이미지) | ~$0.003 |
| Runway (영상 10초) | ~$0.50 |
| **합계** | **~$0.59** |

월 30개 = 약 $18 (~2.4만원)
