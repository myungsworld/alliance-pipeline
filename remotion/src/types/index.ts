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
  durationInFrames: 150, // 5초
};

// ============================================
// 슬롯머신 Composition 타입
// ============================================
export interface SlotMachineProps {
  boss: string;
  hero: string;
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
