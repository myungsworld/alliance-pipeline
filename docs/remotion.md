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

## 기본 설정

```typescript
// 숏폼 기본값 (9:16)
width: 1080
height: 1920
fps: 30
```

---

## 컴포지션 목록

### 1. SlotMachine

슬롯머신 스타일 Boss vs Hero 대결 인트로

**API 요청:**
```json
{
  "compositionId": "SlotMachine",
  "props": {
    "boss": "Angry Mom",
    "hero": "Baby Chick",
    "seed": 12345,
    "audioSrc": "audio/slot-machine-sfx.mp3",
    "audioVolume": 0.8
  },
  "outputPath": "/data/media/intro.mp4"
}
```

**Props:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| boss | string | O | 보스 이름 (슬롯 최종값) |
| hero | string | O | 히어로 이름 (슬롯 최종값) |
| seed | number | X | 슬롯 셔플 시드 (동일 시드 = 동일 애니메이션) |
| audioSrc | string | X | 오디오 파일 경로 (public 폴더 기준) |
| audioVolume | number | X | 볼륨 0-1 (기본: 1) |

**기본 duration:** 195 프레임 (6.5초)

**애니메이션:**
- 타이틀 페이드인 (0.8초)
- 슬롯 릴 회전 (보스 3초, 히어로 3.8초)
- VS 펄스 효과
- 조명 깜빡임

**슬롯 옵션 (config.ts에서 수정):**
```typescript
BOSS_OPTIONS = ["Angry Mom", "Monday Morning", "Alarm Clock", ...]
HERO_OPTIONS = ["Baby Chick", "Sleepy Cat", "Confused Dog", ...]
```

---

### 2. SlotMachineWithEffect

SlotMachine + 줌인 페이드아웃 효과 (다음 장면 연결용)

**API 요청:**
```json
{
  "compositionId": "SlotMachineWithEffect",
  "props": {
    "boss": "Monday Morning",
    "hero": "Coffee Cup",
    "seed": 12345,
    "audioSrc": "audio/slot-machine-sfx.mp3",
    "audioVolume": 0.8,
    "audioStartFrame": 30
  },
  "outputPath": "/data/media/intro_with_effect.mp4"
}
```

**Props:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| boss | string | O | 보스 이름 |
| hero | string | O | 히어로 이름 |
| seed | number | X | 슬롯 셔플 시드 |
| audioSrc | string | X | 오디오 파일 경로 (public 폴더 기준) |
| audioVolume | number | X | 볼륨 0-1 (기본: 1) |
| audioStartFrame | number | X | 오디오 시작 프레임 (기본: 30 = 1초) |

**기본 duration:** 240 프레임 (8초)

**타이밍:**
| 구간 | 프레임 | 시간 |
|------|--------|------|
| 슬롯 시작 | 30 | 1.0초 |
| Boss 멈춤 | 120 | 4.0초 |
| Hero 멈춤 | 159 | 5.3초 |
| 줌 효과 시작 | 195 | 6.5초 |
| 페이드 투 블랙 | 240 | 8.0초 |

---

### 3. StitchMedia

여러 미디어(영상/이미지)를 트랜지션과 함께 연결

**API 요청:**
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

**Props:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| media | MediaItem[] | O | 미디어 배열 |
| transition | TransitionType | X | 트랜지션 효과 (기본: crossfade) |
| transitionDuration | number | X | 트랜지션 길이 프레임 (기본: 15) |

**MediaItem:**
```typescript
{
  type: 'video' | 'image',
  src: string,           // /data/media/xxx
  durationInFrames: number
}
```

**트랜지션 효과:**
| 효과 | 설명 |
|------|------|
| crossfade | 부드러운 페이드 전환 (기본) |
| zoom | 줌 아웃/인 + 페이드 |
| slide-left | 왼쪽으로 슬라이드 |
| slide-right | 오른쪽으로 슬라이드 |
| none | 트랜지션 없이 바로 전환 |

**duration:** 자동 계산 (총 미디어 길이 - 오버랩)

---

### 4. ImageReveal 효과들

이미지를 다양한 효과로 등장시키는 컴포지션들

#### SketchToColor
스케치에서 컬러로 변환되는 효과

```json
{
  "compositionId": "SketchToColor",
  "props": { "src": "/data/media/image.jpg" },
  "outputPath": "/data/media/reveal.mp4"
}
```

#### ParticleAssembly
파티클이 모여서 이미지가 조립되는 효과

```json
{
  "compositionId": "ParticleAssembly",
  "props": { "src": "/data/media/image.jpg", "gridSize": 15 },
  "outputPath": "/data/media/reveal.mp4"
}
```

#### BrushReveal
브러시로 칠하듯 이미지가 드러나는 효과

```json
{
  "compositionId": "BrushReveal",
  "props": { "src": "/data/media/image.jpg" },
  "outputPath": "/data/media/reveal.mp4"
}
```

---

## 새 컴포지션 추가

1. `src/compositions/NewComp/` 폴더 생성
2. `src/types/index.ts`에 Props 타입 정의
3. `src/Root.tsx`에 Composition 등록
4. **이 문서에 컴포지션 정보 추가**

```typescript
// types/index.ts
export interface NewCompProps {
  // props 정의
}

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

---

## 미디어 파일 경로

### 비디오/이미지 (동적)
| 위치 | 경로 |
|------|------|
| Docker 볼륨 | `./media:/data/media` |
| 코드에서 | `/data/media/xxx.mp4` |
| HTTP 접근 | `http://localhost:3001/media/xxx.mp4` |

`MediaRenderer.resolveSrc()`가 `/data/media/` → HTTP URL 자동 변환

### 오디오 (정적, Git 포함)
| 위치 | 경로 |
|------|------|
| 파일 위치 | `remotion/public/audio/` |
| props에서 | `"audioSrc": "audio/xxx.mp3"` |

`staticFile()`로 public 폴더 파일 접근. 렌더링 시 자동으로 번들에 포함됨.

---

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

---

## Docker 환경 주의사항

- `Video` 대신 `OffthreadVideo` 사용 (FFmpeg 기반)
- n8n에서 호출 시 `http://remotion:3001/render` (Docker 네트워크)
