// ============================================
// 공통 비디오 설정
// ============================================
export interface VideoConfig {
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
}

// 기본 숏폼 설정 (9:16)
export const DEFAULT_VIDEO_CONFIG: VideoConfig = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 195, // 6.5초
};

// ============================================
// 슬롯머신 Composition 타입
// ============================================
export interface SlotMachineProps {
  boss: string;
  hero: string;
  seed?: number;  // 슬롯 셔플용 시드 (n8n에서 timestamp 등 전달)
}

// ============================================
// StitchMedia Composition 타입
// ============================================
export type TransitionType = 'crossfade' | 'zoom' | 'slide-left' | 'slide-right' | 'none';

export interface MediaItem {
  type: 'video' | 'image';
  src: string;              // 파일 경로 (/data/media/xxx)
  durationInFrames: number; // 표시 시간 (프레임)
}

export interface StitchMediaProps {
  media: MediaItem[];
  transition?: TransitionType;       // 기본: crossfade
  transitionDuration?: number;       // 트랜지션 프레임 (기본: 15)
}

// ============================================
// 렌더링 요청 타입 (API용)
// ============================================
export interface RenderRequest {
  compositionId: string;  // "SlotMachine", "BattleIntro" 등
  props: Record<string, unknown>;
  outputPath: string;
}

export interface RenderResponse {
  success: boolean;
  outputPath?: string;
  error?: string;
}

// ============================================
// 나중에 추가될 Composition 타입들 예시
// ============================================
// export interface BattleIntroProps {
//   boss: string;
//   hero: string;
//   imagePath: string;
// }
//
// export interface ResultScreenProps {
//   winner: 'boss' | 'hero';
//   score: number;
// }
