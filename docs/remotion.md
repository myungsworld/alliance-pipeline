# Remotion 영상 렌더링

React 기반 프로그래매틱 영상 생성 시스템. n8n에서 HTTP 요청으로 호출하여 영상을 렌더링합니다.

## 설치 및 실행

```bash
cd remotion
npm install
```

**개발 모드 (Remotion Studio):**
```bash
npm run dev
# http://localhost:3000 에서 미리보기 UI 실행
```

**프로덕션 서버:**
```bash
npm run server
# http://localhost:3001 에서 API 서버 실행
```

## API 사용법

**렌더링 요청:**
```bash
curl -X POST http://localhost:3001/render \
  -H "Content-Type: application/json" \
  -d '{
    "compositionId": "SlotMachine",
    "props": {
      "boss": "Angry Mom",
      "hero": "Baby Chick"
    },
    "outputPath": "/tmp/output.mp4"
  }'
```

**헬스체크:**
```bash
curl http://localhost:3001/health
```

## 컴포지션

| ID          | 설명                          | Props                    |
| ----------- | ----------------------------- | ------------------------ |
| SlotMachine | 슬롯머신 스타일 대결 인트로   | `boss`, `hero`           |

## 파일 구조

```
remotion/
├── package.json
├── tsconfig.json
├── remotion.config.ts
└── src/
    ├── index.ts              # Remotion 번들러 진입점
    ├── Root.tsx              # 컴포지션 등록
    ├── types.ts              # 타입 정의
    ├── server/
    │   └── index.ts          # Express API 서버
    └── compositions/
        └── SlotMachine/
            ├── index.tsx     # 메인 컴포지션
            ├── SlotReel.tsx  # 슬롯 릴 애니메이션
            └── config.ts     # 설정 (색상, 타이밍, 옵션)
```

## 주요 기술 개념

### Remotion 핵심 API

- **useCurrentFrame()**: 현재 프레임 번호 반환 (애니메이션 기준)
- **interpolate()**: 프레임 → 애니메이션 값 매핑
- **Easing.bezier()**: 커스텀 이징 곡선 (easeOutQuint 등)
- **AbsoluteFill**: 전체 화면 채우는 컨테이너

### 성능 최적화

- **useMemo**: 매 프레임 재계산 방지 (슬롯 아이템 셔플 등)
- **Seeded Shuffle**: Fisher-Yates + 시드 기반 결정적 랜덤

### 렌더링 파이프라인

```
n8n HTTP 요청 → Express 서버 → @remotion/bundler → @remotion/renderer → 출력 파일
```

## n8n 연동 예시

n8n HTTP Request 노드 설정:
- Method: POST
- URL: http://localhost:3001/render
- Body:
```json
{
  "compositionId": "SlotMachine",
  "props": {
    "boss": "{{ $json.boss_name }}",
    "hero": "{{ $json.hero_name }}"
  },
  "outputPath": "/tmp/videos/battle_{{ $json.id }}.mp4"
}
```
