# Remotion 영상 렌더링

React 기반 프로그래매틱 영상 생성 시스템

## 실행

```bash
# 개발 모드 (Remotion Studio)
cd remotion && npm run dev    # http://localhost:3000

# 프로덕션 서버
npm run server                # http://localhost:3001

# Docker
docker compose up remotion -d
```

## 컴포지션

### SlotMachine

슬롯머신 스타일 대결 인트로

```json
{
  "compositionId": "SlotMachine",
  "props": {
    "boss": "Angry Mom",
    "hero": "Baby Chick",
    "seed": 12345
  },
  "outputPath": "/data/media/intro.mp4"
}
```

### StitchMedia

미디어 연결 + 트랜지션

```json
{
  "compositionId": "StitchMedia",
  "props": {
    "media": [
      { "type": "video", "src": "/data/media/template.mp4", "durationInFrames": 195 },
      { "type": "image", "src": "/data/media/boss.jpg", "durationInFrames": 150 }
    ],
    "transition": "crossfade",
    "transitionDuration": 15
  },
  "outputPath": "/data/media/final.mp4"
}
```

**트랜지션:**
- `crossfade` - 페이드 전환 (기본)
- `zoom` - 줌 + 페이드
- `slide-left` / `slide-right` - 슬라이드
- `none` - 바로 전환

## 새 컴포지션 추가

1. `src/compositions/NewComp/` 폴더 생성
2. `src/types/index.ts`에 Props 타입 정의
3. `src/Root.tsx`에 Composition 등록

```typescript
// Root.tsx
<Composition
  id="NewComp"
  component={NewComp}
  fps={DEFAULT_VIDEO_CONFIG.fps}
  width={DEFAULT_VIDEO_CONFIG.width}
  height={DEFAULT_VIDEO_CONFIG.height}
  durationInFrames={300}
  defaultProps={{ ... }}
/>
```

## 미디어 파일 경로

| 위치           | 경로                                |
| -------------- | ----------------------------------- |
| Docker 볼륨    | `./media:/data/media`               |
| 코드에서       | `/data/media/xxx.mp4`               |
| HTTP 접근      | `http://localhost:3001/media/xxx.mp4` |

MediaRenderer의 `resolveSrc()`가 자동 변환

## Docker 환경 주의사항

- `Video` 대신 `OffthreadVideo` 사용 (FFmpeg 기반)
- n8n에서 호출 시 `http://remotion:3001/render` (Docker 네트워크)

## API

**POST /render**
```bash
curl -X POST http://localhost:3001/render \
  -H "Content-Type: application/json" \
  -d '{ "compositionId": "...", "props": {...}, "outputPath": "..." }'
```

**응답:**
```json
{ "success": true, "outputPath": "/data/media/output.mp4" }
```

**GET /health**
```json
{ "status": "ok" }
```
