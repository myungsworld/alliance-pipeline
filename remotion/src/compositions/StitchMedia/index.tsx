// ============================================
// StitchMedia 컴포지션
// 여러 미디어(영상/이미지)를 연결하여 하나의 영상으로 만듦
// ============================================
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate } from 'remotion';
import { StitchMediaProps, MediaItem } from '../../types';
import { MediaRenderer } from './MediaRenderer';

// 타이밍 정보가 포함된 미디어 아이템
interface MediaWithTiming extends MediaItem {
  startFrame: number;
  endFrame: number;
}

// 총 영상 길이 계산 (트랜지션 오버랩 고려)
export const calculateTotalDuration = (
  media: MediaItem[],
  transitionDuration: number
): number => {
  if (media.length === 0) return 0;

  const totalFrames = media.reduce((acc, item) => acc + item.durationInFrames, 0);
  const overlaps = (media.length - 1) * transitionDuration;
  return totalFrames - overlaps;
};

export const StitchMedia: React.FC<StitchMediaProps> = ({
  media,
  transition = 'crossfade',
  transitionDuration = 15,
}) => {
  const frame = useCurrentFrame();

  // 각 미디어의 시작/종료 프레임 계산
  const mediaWithTiming: MediaWithTiming[] = [];
  let currentFrame = 0;

  media.forEach((item, index) => {
    const startFrame = currentFrame;
    const endFrame = startFrame + item.durationInFrames;

    mediaWithTiming.push({
      ...item,
      startFrame,
      endFrame,
    });

    // 다음 미디어는 트랜지션만큼 오버랩 시작
    const overlap = index < media.length - 1 ? transitionDuration : 0;
    currentFrame += item.durationInFrames - overlap;
  });

  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {mediaWithTiming.map((item, index) => {
        const isActive = frame >= item.startFrame && frame < item.endFrame;
        if (!isActive) return null;

        const localFrame = frame - item.startFrame;
        const transitionOutStart = item.durationInFrames - transitionDuration;

        // 트랜지션 진행도 계산
        let transitionProgress = 0;
        let isTransitionOut = false;

        // 들어오는 트랜지션 (첫 번째 제외)
        if (index > 0 && localFrame < transitionDuration) {
          transitionProgress = interpolate(
            localFrame,
            [0, transitionDuration],
            [0, 1],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          );
        }
        // 나가는 트랜지션 (마지막 제외)
        else if (index < media.length - 1 && localFrame >= transitionOutStart) {
          transitionProgress = interpolate(
            localFrame,
            [transitionOutStart, item.durationInFrames],
            [0, 1],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          );
          isTransitionOut = true;
        }

        return (
          <Sequence
            key={index}
            from={item.startFrame}
            durationInFrames={item.durationInFrames}
          >
            <AbsoluteFill>
              <MediaRenderer
                item={item}
                transitionProgress={transitionProgress}
                transitionType={transition}
                isTransitionOut={isTransitionOut}
              />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
