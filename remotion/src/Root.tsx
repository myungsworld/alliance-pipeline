// ============================================
// Remotion 진입점
// 모든 컴포지션을 등록하는 파일
// ============================================
import { Composition } from 'remotion';
import { SlotMachine } from './compositions/SlotMachine';
import { DEFAULT_VIDEO_CONFIG } from './types';

export const RemotionRoot: React.FC = () => {
  return (
    <>
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
        }}
      />
      {/* 나중에 다른 컴포지션 추가 */}
      {/* <Composition id="BattleIntro" ... /> */}
    </>
  );
};
