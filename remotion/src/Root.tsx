// ============================================
// Remotion 진입점
// 모든 컴포지션을 등록하는 파일
// ============================================
import { Composition } from 'remotion';
import { SlotMachine } from './compositions/SlotMachine';
import { SlotMachineWithEffect, SLOT_MACHINE_WITH_EFFECT_DURATION } from './compositions/SlotMachineWithEffect';
import { StitchMedia, calculateTotalDuration } from './compositions/StitchMedia';
import {
  SketchToColor, SKETCH_TO_COLOR_DURATION,
  ParticleAssembly, PARTICLE_ASSEMBLY_DURATION,
  BrushReveal, BRUSH_REVEAL_DURATION,
} from './compositions/ImageReveal';
import { DEFAULT_VIDEO_CONFIG, StitchMediaProps } from './types';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 슬롯머신 인트로 */}
      <Composition
        id="SlotMachine"
        component={SlotMachine as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={DEFAULT_VIDEO_CONFIG.durationInFrames}
        fps={DEFAULT_VIDEO_CONFIG.fps}
        width={DEFAULT_VIDEO_CONFIG.width}
        height={DEFAULT_VIDEO_CONFIG.height}
        defaultProps={{
          boss: "Monday Morning",
          hero: "Coffee Cup",
          seed: 12345,
        }}
      />

      {/* 슬롯머신 + 줌인 페이드아웃 (다음 장면 연결용) */}
      <Composition
        id="SlotMachineWithEffect"
        component={SlotMachineWithEffect as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={SLOT_MACHINE_WITH_EFFECT_DURATION}
        fps={DEFAULT_VIDEO_CONFIG.fps}
        width={DEFAULT_VIDEO_CONFIG.width}
        height={DEFAULT_VIDEO_CONFIG.height}
        defaultProps={{
          boss: "Monday Morning",
          hero: "Coffee Cup",
          seed: 12345,
        }}
      />

      {/* 미디어 연결 (영상+이미지, 영상+영상 등) */}
      <Composition
        id="StitchMedia"
        component={StitchMedia as unknown as React.FC<Record<string, unknown>>}
        fps={DEFAULT_VIDEO_CONFIG.fps}
        width={DEFAULT_VIDEO_CONFIG.width}
        height={DEFAULT_VIDEO_CONFIG.height}
        durationInFrames={300}
        calculateMetadata={async ({ props }) => {
          const p = props as unknown as StitchMediaProps;
          const duration = calculateTotalDuration(p.media || [], p.transitionDuration || 15);
          return { durationInFrames: duration || 300 };
        }}
        defaultProps={{
          media: [
            { type: 'video', src: '/data/media/template_1.mp4', durationInFrames: 195 },
            { type: 'image', src: '/data/media/boss_1.jpg', durationInFrames: 150 },
          ],
          transition: 'crossfade',
          transitionDuration: 15,
        }}
      />

      {/* ============================================ */}
      {/* Image Reveal 효과들 */}
      {/* ============================================ */}

      {/* 1. 스케치 → 컬러 */}
      <Composition
        id="SketchToColor"
        component={SketchToColor as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={SKETCH_TO_COLOR_DURATION}
        fps={DEFAULT_VIDEO_CONFIG.fps}
        width={DEFAULT_VIDEO_CONFIG.width}
        height={DEFAULT_VIDEO_CONFIG.height}
        defaultProps={{
          src: '/data/media/boss_5_eraser_vs_pencil.jpg',
        }}
      />

      {/* 2. 파티클 조립 */}
      <Composition
        id="ParticleAssembly"
        component={ParticleAssembly as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={PARTICLE_ASSEMBLY_DURATION}
        fps={DEFAULT_VIDEO_CONFIG.fps}
        width={DEFAULT_VIDEO_CONFIG.width}
        height={DEFAULT_VIDEO_CONFIG.height}
        defaultProps={{
          src: '/data/media/boss_5_eraser_vs_pencil.jpg',
          gridSize: 15,
        }}
      />

      {/* 3. 브러시 리빌 */}
      <Composition
        id="BrushReveal"
        component={BrushReveal as unknown as React.FC<Record<string, unknown>>}
        durationInFrames={BRUSH_REVEAL_DURATION}
        fps={DEFAULT_VIDEO_CONFIG.fps}
        width={DEFAULT_VIDEO_CONFIG.width}
        height={DEFAULT_VIDEO_CONFIG.height}
        defaultProps={{
          src: '/data/media/boss_5_eraser_vs_pencil.jpg',
        }}
      />
    </>
  );
};
