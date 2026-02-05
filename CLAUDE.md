# Claude 작업 기록

이 문서는 Claude와 함께 작업한 내용을 정리한 기록입니다.

## 프로젝트 개요

AI 기반 숏폼 콘텐츠 자동 생성 파이프라인. n8n 워크플로우로 텔레그램 입력을 받아 LLM으로 스토리 생성, 이미지 생성, 영상 렌더링까지 자동화합니다.

## 핵심 설계 원칙

### 확장 가능한 Remotion 구조

새로운 컴포지션 추가 시:
1. `remotion/src/compositions/` 아래 폴더 생성
2. `remotion/src/types/index.ts`에 Props 타입 정의
3. `remotion/src/Root.tsx`에 Composition 등록
4. **`docs/remotion.md`에 컴포지션 문서 추가** ← 필수!

```typescript
// 새 컴포지션 추가 예시
<Composition
  id="NewComposition"
  component={NewComposition}
  fps={DEFAULT_VIDEO_CONFIG.fps}
  width={DEFAULT_VIDEO_CONFIG.width}
  height={DEFAULT_VIDEO_CONFIG.height}
  durationInFrames={300}
  defaultProps={{ ... }}
/>
```

**현재 구현된 컴포지션:** → 상세 문서: [docs/remotion.md](../docs/remotion.md)
| ID | 설명 | 주요 Props |
|----|------|-----------|
| SlotMachine | 슬롯머신 대결 인트로 | boss, hero, seed |
| StitchMedia | 미디어 연결 + 트랜지션 | media[], transition, transitionDuration |

### 미디어 파일 경로 규칙

- Docker 볼륨: `./media:/data/media`
- 코드에서 경로: `/data/media/xxx.mp4`
- Remotion 내부 HTTP 접근: `http://localhost:3001/media/xxx.mp4`
- MediaRenderer의 `resolveSrc()`가 자동 변환

## 작업 히스토리

### 2026-02-05: bosses 테이블 + StitchMedia 컴포지션

**요청:** 보스전 모드 추가 - 템플릿 영상과 생성된 이미지를 연결하는 기능

**완료:**
1. `db/03_bosses.sql` - bosses 테이블 생성
   - input_boss, input_hero: 원본 입력
   - boss_name, hero_name, boss_description, hero_description, location: LLM 생성
   - template: 템플릿 영상 경로
   - img_url: 생성된 이미지 경로

2. `remotion/src/compositions/StitchMedia/` - 미디어 연결 컴포지션
   - index.tsx: 메인 컴포지션 (타이밍 계산, Sequence 배치)
   - MediaRenderer.tsx: 비디오/이미지 렌더링 (OffthreadVideo, Img)
   - transitions.ts: 트랜지션 효과 (crossfade, zoom, slide-left, slide-right, none)

3. `remotion/src/server/index.ts` 수정
   - CORS 헤더 추가 (Range 요청 지원)
   - `/media` 정적 파일 서빙 추가

**트러블슈팅:**
- Docker에서 Video 컴포넌트 재생 안됨 → `OffthreadVideo` 사용 (FFmpeg 기반)
- 트랜지션 중 검은색 섞임 → crossfade에서 나가는 미디어는 opacity 1 유지

### StitchMedia 트랜지션 로직

```
[Media 1: 0-195프레임]
              [오버랩: 180-195] ← 트랜지션 구간
        [Media 2: 180-330프레임]

총 길이 = 195 + 150 - 15(오버랩) = 330 프레임
```

트랜지션 중:
- 나가는 미디어(아래): opacity 1 유지
- 들어오는 미디어(위): opacity 0→1 페이드인
- 이렇게 해야 CSS opacity 스태킹에서 검은색이 안 섞임

## API 레퍼런스

### Remotion 렌더링 API

**POST /render**
```json
{
  "compositionId": "StitchMedia",
  "props": {
    "media": [
      { "type": "video", "src": "/data/media/template_1.mp4", "durationInFrames": 195 },
      { "type": "image", "src": "/data/media/boss_1.jpg", "durationInFrames": 150 }
    ],
    "transition": "crossfade",
    "transitionDuration": 15
  },
  "outputPath": "/data/media/final_1.mp4"
}
```

**트랜지션 효과:**
| 효과        | 설명                         |
| ----------- | ---------------------------- |
| crossfade   | 부드러운 페이드 (기본값)     |
| zoom        | 줌 아웃/인 + 페이드          |
| slide-left  | 왼쪽 슬라이드                |
| slide-right | 오른쪽 슬라이드              |
| none        | 바로 전환                    |

### n8n에서 Remotion 호출

Docker 네트워크에서는 `localhost` 대신 `remotion` 사용:
```
http://remotion:3001/render
```

## 워크플로우 구조

### new-boss (보스전)

```
[Telegram boss-bot 입력: "보스 vs 히어로"]
    ↓
[Gemini LLM: 캐릭터/배경 생성]
    ↓
[DB 저장: bosses 테이블]
    ↓
[Replicate: 이미지 생성]
    ↓
[Execute Command: wget으로 이미지 저장]
    ↓
[DB 업데이트: img_url]
    ↓
[Telegram: 이미지 + "영상 생성" 버튼]
    ↓
[버튼 클릭]
    ↓
[Remotion StitchMedia: 템플릿 영상 + 이미지 합성]
    ↓
[최종 영상 출력: /data/media/final_N.mp4]
```

## 타입 정의

```typescript
// remotion/src/types/index.ts

export type TransitionType = 'crossfade' | 'zoom' | 'slide-left' | 'slide-right' | 'none';

export interface MediaItem {
  type: 'video' | 'image';
  src: string;              // /data/media/xxx
  durationInFrames: number;
}

export interface StitchMediaProps {
  media: MediaItem[];
  transition?: TransitionType;
  transitionDuration?: number;
}
```

## TODO

- [ ] 보스전 완성 영상 → Telegram 전송
- [ ] 트랜지션 스무스함 검증
- [ ] 서버 배포 (Oracle Cloud)

---

## 문서 업데이트 규칙

새로운 기능 추가 시 업데이트할 문서:
- **Remotion 컴포지션 추가** → `docs/remotion.md` 컴포지션 목록에 추가
- **DB 테이블 추가** → 이 문서 작업 히스토리에 기록
- **워크플로우 추가** → 이 문서 워크플로우 구조에 기록
