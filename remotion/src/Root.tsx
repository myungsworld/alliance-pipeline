// ============================================
// Remotion 진입점
// 모든 컴포지션을 등록하는 파일
// ============================================
import { Composition } from 'remotion';
import { SlotMachine } from './compositions/SlotMachine';
import { StitchMedia, calculateTotalDuration } from './compositions/StitchMedia';
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
    </>
  );
};
