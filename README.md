# Alliance Pipeline

AI 숏폼 콘텐츠 자동 생성 파이프라인

## 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Docker Compose                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Telegram │───▶│   n8n    │───▶│ Remotion │───▶│  Output  │      │
│  │   Bot    │    │ Workflow │    │  Server  │    │  Media   │      │
│  └──────────┘    └────┬─────┘    └──────────┘    └──────────┘      │
│                       │                                              │
│         ┌─────────────┼─────────────┐                               │
│         ▼             ▼             ▼                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                          │
│  │ Postgres │  │  Gemini  │  │Replicate │                          │
│  │    DB    │  │   LLM    │  │  Image   │                          │
│  └──────────┘  └──────────┘  └──────────┘                          │
│                                                                      │
│  ┌──────────┐                                                       │
│  │  ngrok   │  Webhook 터널링                                       │
│  └──────────┘                                                       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 파이프라인 흐름

```
[사용자 입력]     "월요병 vs 커피"
      │
      ▼
[n8n Workflow]    Telegram → 파싱 → DB 저장
      │
      ▼
[LLM 생성]        Gemini → 캐릭터/스토리/배경 생성
      │
      ▼
[이미지 생성]     Replicate Flux → 이미지 저장
      │
      ▼
[영상 렌더링]     Remotion → 템플릿 + 이미지 합성
      │
      ▼
[결과 전송]       Telegram → 사용자
```

## 빠른 시작

```bash
cp .env.example .env    # 환경변수 설정
docker compose up -d    # 서비스 시작
./scripts/sync-to-n8n.sh # 워크플로우 동기화
```

## 서비스 구성

| 서비스     | 포트  | 역할                          |
| ---------- | ----- | ----------------------------- |
| n8n        | 5678  | 워크플로우 오케스트레이션     |
| PostgreSQL | 5432  | 데이터 저장 (시드 데이터 포함) |
| Remotion   | 3001  | 영상 렌더링 API               |
| ngrok      | 4040  | Webhook 터널링                |

## 프로젝트 구조

```
alliance-pipeline/
├── docker-compose.yaml     # 서비스 정의
├── .env                    # 환경변수
│
├── workflows/              # n8n 워크플로우
│   ├── alliance-pipeline/  # 조우/대결 모드
│   └── new-boss/           # 보스전 모드
│
├── db/                     # PostgreSQL 스키마 & 시드
│   ├── 01_seed_objects.sql # 물건 251개
│   └── 02_seed_creatures.sql # 생명체 231개
│
├── remotion/               # 영상 렌더링 서버
│   └── src/compositions/   # 컴포지션 (SlotMachine, StitchMedia)
│
├── scripts/                # 유틸리티 (sync, export, pre-commit)
├── credentials/            # n8n credentials
└── media/                  # 생성된 미디어 파일
```

## 문서

- [IDEAS.md](IDEAS.md) - 프로젝트 컨셉 & 아이디어
- [CLAUDE.md](CLAUDE.md) - 개발 히스토리 & API 레퍼런스
- [docs/remotion.md](docs/remotion.md) - Remotion 상세 문서
