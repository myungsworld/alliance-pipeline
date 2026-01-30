# AI 숏폼 자동화 파이프라인

n8n + Telegram + Google Gemini를 활용한 AI 숏폼 콘텐츠 자동 생성 시스템

## 컨셉

**랜덤 물건 + 랜덤 생명체** 조합으로 예측 불가능한 재미있는 숏폼 콘텐츠 자동 생성

### 두 가지 컨텐츠 모드

| 모드     | 설명                                      | 예시                          |
| -------- | ----------------------------------------- | ----------------------------- |
| **조우** | 생명체가 물건을 마주했을 때 벌어지는 상황 | 펭귄 + 우산 → 5가지 웃긴 상황 |
| **대결** | 두 조합이 맞붙는 시나리오                 | 칼 든 치킨 vs 방패 든 고양이  |

## 기술 스택

| 구성요소          | 기술              |
| ----------------- | ----------------- |
| 워크플로우 자동화 | n8n (self-hosted) |
| 데이터베이스      | PostgreSQL 16     |
| LLM               | Google Gemini     |
| 메신저 봇         | Telegram Bot API  |
| 터널링            | ngrok (Webhook용) |
| 컨테이너          | Docker Compose    |

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

### 3. Pre-commit Hook 설정

```bash
ln -sf ../../scripts/pre-commit.sh .git/hooks/pre-commit
```

### 4. Docker 실행

```bash
docker compose up -d
```

### 5. n8n 동기화

```bash
./scripts/sync-to-n8n.sh
```

기존 credentials/workflows를 모두 삭제하고 로컬 JSON에서 새로 import합니다.

## 사용 방법

텔레그램 봇에게 메시지를 보내면 동작합니다.

**조우 모드:**

1. **"조우"** 전송 → 10개 랜덤 조합 버튼 표시
2. 원하는 조합 클릭 → Gemini가 5가지 상황 생성
3. **"이미지 생성"** 또는 **"다른 시나리오"** 선택

**대결 모드:**

1. **"대결"** 전송 → 5개 vs 버튼 표시
2. 원하는 대결 클릭 → Gemini가 대결 시나리오 생성

## 워크플로우 구조

단일 워크플로우 (`alliance-pipeline`) - 2개 트리거, 27개 노드

### Trigger 1: start channel (message + callback_query)

```
[Telegram] → [메인 라우터]
  ├─ "조우"   → [랜덤조합 쿼리] → [조우 버튼 생성] → [텔레그램 전송]
  ├─ "대결"   → [대결 쿼리] → [대결 버튼 생성] → [텔레그램 전송]
  ├─ select_  → [조우 파싱] → [DB 조회] → [Gemini LLM] → [DB 저장] → [시나리오 포맷] → [script-bot 전송]
  └─ vs_      → [대결 파싱] → [DB 조회] → [Gemini LLM] → [script-bot 전송]
```

### Trigger 2: script button handler (callback_query)

```
[script-bot Callback] → [이미지 라우터]
  └─ encounter_ → [DB 조회] → [Replicate 이미지 생성] → [Wait] → [결과 확인] → [이미지 전송/재시도]
```

## 멀티 PC 동기화

### 작업 흐름

```
[PC A: n8n에서 작업] → git commit (pre-commit hook이 자동 export) → git push
                                                                        ↓
[PC B: git pull] → docker compose up -d → ./scripts/sync-to-n8n.sh → 작업 시작
```

**pre-commit hook이 자동으로:**

- n8n에서 credentials export → `credentials/credentials.json`
- n8n에서 workflows export → `workflows/*.json`
- 변경된 파일을 staging에 추가

**다른 PC에서 동기화:**

```bash
git pull
docker compose up -d
./scripts/sync-to-n8n.sh
```

### 스크립트

| 스크립트                | 설명                                                    |
| ----------------------- | ------------------------------------------------------- |
| `sync-to-n8n.sh`        | credentials + workflows를 n8n에 동기화 (삭제 후 import) |
| `export-credentials.sh` | n8n → `credentials/credentials.json` 내보내기           |
| `export-workflow.sh`    | n8n → `workflows/*.json` 내보내기                       |
| `pre-commit.sh`         | git commit 시 자동 export (hook)                        |

## 데이터베이스

### 테이블

```sql
objects (id, name, name_en, category, category_en, created_at)           -- 물건 251개, 20개 카테고리
creatures (id, name, name_en, category, category_en, created_at)         -- 생명체 231개, 15개 카테고리
combinations_used (id, object_id, creature_id, content_type, used_at)
encounter_scripts (id, object_id, creature_id, object_name, object_name_en,
                   creature_name, creature_name_en, character_description,
                   situations JSONB, selected_index, image_url, video_url,
                   status, created_at, updated_at)
```

### situations JSONB 구조

```json
{
  "situations": [
    {
      "situation_eng": "The robot pokes the pencil with its metal finger",
      "situation_kor": "로봇이 금속 손가락으로 연필을 찌른다",
      "reaction_type": "curiosity",
      "caption_kor": "이게 뭐지...?"
    }
  ]
}
```

- `situation_eng/kor`: 상황 설명 (내레이션, 음성용)
- `reaction_type`: 감정 반응 (이미지/영상 표정 자동 매핑)
- `caption_kor`: 짧은 반응 (자막용)

### Reaction Type 매핑

| reaction_type | 이미지 프롬프트 | 영상 프롬프트 |
|---------------|-----------------|---------------|
| curiosity | head tilted with wide curious eyes | curious slow movement |
| surprise | jumping back with eyes wide open | sudden startled jump |
| confusion | scratching head bewildered | hesitant confused motion |
| frustration | angry stance narrowed eyes | angry agitated movement |
| fear | cowering trembling | trembling cowering |
| delight | happy bounce sparkling eyes | happy bouncing |

- `name` / `category`: 한국어 (텔레그램 표시용)
- `name_en` / `category_en`: 영어 (API 프롬프트용)

### PostgreSQL 접속 정보

| 필드            | 값                                |
| --------------- | --------------------------------- |
| Host            | `postgres` (Docker 내부 네트워크) |
| Database        | `content_db`                      |
| User / Password | `.env` 파일 참조                  |
| Port            | `5432`                            |

## 파일 구조

```
alliance-pipeline/
├── docker-compose.yaml       # Docker 설정 (n8n, postgres, ngrok)
├── .env                      # 환경변수 (git 제외)
├── .env.example              # 환경변수 템플릿
├── init.sql                  # DB 스키마 + 시드 데이터
├── workflows/                # n8n 워크플로우 백업 (JSON)
├── credentials/              # n8n credentials (환경변수 참조)
│   └── credentials.json
├── scripts/
│   ├── sync-to-n8n.sh        # n8n 동기화 (credentials + workflows)
│   ├── export-credentials.sh # credentials 내보내기
│   ├── export-workflow.sh    # 워크플로우 내보내기
│   └── pre-commit.sh         # git pre-commit hook
└── README.md
```

## 접속 URL

| 서비스         | URL                   |
| -------------- | --------------------- |
| n8n            | http://localhost:5678 |
| ngrok 대시보드 | http://localhost:4040 |
| PostgreSQL     | localhost:5432        |

## 진행 상황

### 완료

- [x] Docker 환경 구성 (n8n + PostgreSQL + ngrok)
- [x] DB 스키마 및 시드 데이터 (물건 251개, 생명체 231개)
- [x] Telegram Bot 연동
- [x] ngrok HTTPS 터널 설정
- [x] 통합 워크플로우: alliance-pipeline (조우/대결/이미지 생성)
- [x] encounter_scripts 테이블 (LLM 결과 저장)
- [x] 멀티 PC 동기화 (pre-commit hook + sync 스크립트)
- [x] 환경변수 기반 credentials 관리
- [x] 3개 워크플로우 → 1개 통합 (webhook 충돌 해결)
- [x] 이미지 생성 API 연동 (Replicate Flux Dev)
- [x] 영상 생성 API 연동 (Replicate minimax/video-01)
- [x] 캐릭터 일관성 유지 (character_description)
- [x] 연출 시스템 (event + reaction_type 분리)

### 예정

- [ ] reaction 시스템 테스트 및 조정
- [ ] 자동 업로드 (TikTok / YouTube Shorts)
- [ ] 서버 배포 (Oracle Cloud)

## 예상 비용 (콘텐츠 1개당)

| 항목                    | 비용       |
| ----------------------- | ---------- |
| Gemini (스토리)         | ~$0.01     |
| Replicate SDXL (이미지) | ~$0.001    |
| Runway (영상 10초)      | ~$0.50     |
| **합계**                | **~$0.59** |

월 30개 = 약 $18 (~2.4만원)
