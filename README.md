# AI 숏폼 자동화 파이프라인

n8n을 이용한 틱톡/유튜브 숏폼 콘텐츠 자동 생성 및 업로드 시스템

## 컨셉

**랜덤 물건 + 랜덤 생명체** 조합으로 예측 불가능한 재미있는 숏폼 콘텐츠 자동 생성

예시:
- "우산 + 펭귄" → 펭귄이 우산으로 할 수 있는 것들
- "칼을 든 치킨 군대 vs 방패를 든 고양이 군대"

## 기술 스택

- **n8n**: 워크플로우 자동화
- **PostgreSQL**: 물건/생명체 데이터베이스
- **Docker Compose**: 컨테이너 관리

## 현재 진행 상황

### 완료
- [x] Docker 환경 구성 (n8n + PostgreSQL)
- [x] 환경변수 분리 (.env)
- [x] DB 스키마 설계 및 생성
- [x] 초기 데이터 입력 (물건 251개, 생명체 231개)
- [x] 랜덤 조합 뷰 생성

### 진행 예정
- [ ] n8n에서 PostgreSQL 연결 테스트
- [ ] LLM 연동 (스토리 생성)
- [ ] 이미지 생성 API 연동 (DALL-E)
- [ ] 영상 생성 API 연동 (Runway/Kling)
- [ ] 틱톡 업로드 자동화
- [ ] 서버 배포 (Oracle Cloud)

## 로컬 실행 방법

### 1. 환경변수 설정

```bash
cp .env.example .env
# .env 파일에서 POSTGRES_PASSWORD 수정
```

### 2. Docker 실행

```bash
# 시작
docker-compose up -d

# 중지 (데이터 유지)
docker-compose down

# 완전 초기화 (데이터 삭제)
docker-compose down -v
```

### 3. 접속

- **n8n**: http://localhost:5678
- **PostgreSQL**: localhost:5432

## n8n PostgreSQL 연결 정보

| 필드 | 값 |
|------|------|
| Host | `postgres` |
| Database | `content_db` |
| User | `n8n` |
| Password | `.env` 파일 참조 |
| Port | `5432` |
| SSL | `Disable` |

> 주의: Host는 `localhost`가 아니라 `postgres` (Docker 내부 네트워크)

## 데이터베이스 구조

### 테이블

```sql
-- 물건 (251개)
objects (id, name, category, created_at)

-- 생명체 (231개)
creatures (id, name, category, created_at)

-- 사용된 조합 기록
combinations_used (id, object_id, creature_id, content_type, used_at)
```

### 카테고리

**물건 (20개 카테고리)**
- 도구, 가전, 탈것, 악기, 무기, 일상용품, 가구, 스포츠
- 음식, 건물, 자연물, SF, 판타지, 문구, 장난감, 의료, 주방, 캠핑, 전자기기

**생명체 (15개 카테고리)**
- 포유류, 조류, 수중생물, 파충류, 양서류, 곤충
- 상상, 직업, 역사, 신화, 공포, 캐릭터, 공룡, 기계, 기타

### 랜덤 조합 쿼리

```sql
-- 사용 안 된 조합 중 랜덤 1개
SELECT * FROM random_unused_combination;
```

## 예상 워크플로우

```
[Schedule Trigger]
    ↓
[PostgreSQL: 랜덤 조합 가져오기]
    ↓
[LLM: 스토리 생성]
    ↓
[DALL-E: 이미지 생성]
    ↓
[Runway/Kling: 영상 생성]
    ↓
[FFmpeg: 후처리]
    ↓
[TikTok: 업로드]
    ↓
[Telegram: 알림]
```

## 서버 배포 (예정)

### Oracle Cloud Free Tier

- Shape: VM.Standard.A1.Flex
- 사양: 4 OCPU, 24GB RAM
- 비용: 무료

> 현재 San Jose 리전 용량 부족으로 대기 중
> 새벽 시간대에 재시도 필요

## 파일 구조

```
alliance-pipeline/
├── docker-compose.yaml    # Docker 설정
├── .env                   # 환경변수 (git 제외)
├── .env.example           # 환경변수 예시
├── .gitignore
├── init.sql               # DB 초기화 스크립트
├── files/                 # n8n 파일 저장소
├── workflows/             # n8n 워크플로우 백업 (JSON)
├── DEVELOPMENT.md         # 개발 일지
└── README.md              # 이 파일
```

## 다른 컴퓨터에서 환경 설정

### 1. 프로젝트 클론
```bash
git clone https://github.com/your-repo/alliance-pipeline.git
cd alliance-pipeline
```

### 2. 환경변수 설정
```bash
cp .env.example .env
```

`.env` 파일을 열어서 다음 값들을 입력:
```bash
POSTGRES_PASSWORD=your_password
GEMINI_API_KEY=your_gemini_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
NGROK_AUTHTOKEN=your_ngrok_token
WEBHOOK_URL=your_ngrok_url
```

### 3. Docker 실행
```bash
docker compose up -d
```

### 4. n8n 워크플로우 가져오기
1. http://localhost:5678 접속
2. 좌측 메뉴에서 `Import from File` 클릭
3. `workflows/` 폴더의 JSON 파일 선택
4. Credential 재설정 필요:
   - PostgreSQL (Host: `postgres`, DB: `content_db`)
   - Telegram Bot Token
   - Google Gemini API Key

### 5. ngrok 설정 (Telegram Webhook용)
```bash
ngrok http 5678
```
생성된 HTTPS URL을 `.env`의 `WEBHOOK_URL`에 업데이트 후 컨테이너 재시작:
```bash
docker compose down && docker compose up -d
```

## 워크플로우 관리

### 백업/내보내기
워크플로우 수정 후 다음 명령으로 백업:
```bash
docker exec n8n n8n export:workflow --backup --output=/workflows/
```

### 삭제
```bash
# 1. JSON 파일 삭제
rm workflows/워크플로우ID.json

# 2. n8n API로 완전 삭제 (API 키: n8n UI > Settings > API에서 생성)
curl -X DELETE "http://localhost:5678/api/v1/workflows/워크플로우ID" \
  -H "X-N8N-API-KEY: your_api_key"
```

## 예상 비용 (콘텐츠 1개당)

| 항목 | 비용 |
|------|------|
| GPT-4 (스토리) | ~$0.05 |
| DALL-E 3 (이미지 2장) | ~$0.08 |
| Runway (영상 10초) | ~$0.50 |
| **합계** | **~$0.63** |

월 30개 = 약 $19 (2.5만원)
