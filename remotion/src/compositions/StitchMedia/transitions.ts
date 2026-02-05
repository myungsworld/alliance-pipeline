// ============================================
// 트랜지션 효과 유틸리티
// ============================================
import { interpolate, Easing } from 'remotion';
import { TransitionType } from '../../types';

export interface TransitionStyle {
  opacity: number;
  transform: string;
}

// 트랜지션 스타일 계산
export const getTransitionStyle = (
  progress: number,
  type: TransitionType,
  isOutgoing: boolean
): TransitionStyle => {
  if (type === 'none' || progress === 0) {
    return { opacity: 1, transform: 'none' };
  }

  // Easing 적용
  const easedProgress = Easing.inOut(Easing.ease)(progress);

  switch (type) {
    case 'crossfade':
      // 나가는 미디어는 opacity 1 유지 (아래에 깔림)
      // 들어오는 미디어만 fade in (위에서 덮음)
      // 이렇게 해야 중간에 검은색이 섞이지 않음
      return {
        opacity: isOutgoing ? 1 : easedProgress,
        transform: 'none',
      };

    case 'zoom':
      const scale = isOutgoing
        ? interpolate(easedProgress, [0, 1], [1, 1.2])
        : interpolate(easedProgress, [0, 1], [0.8, 1]);
      // crossfade와 동일: 나가는 미디어는 opacity 1 유지
      return {
        opacity: isOutgoing ? 1 : easedProgress,
        transform: `scale(${scale})`,
      };

    case 'slide-left':
      const translateLeft = isOutgoing
        ? interpolate(easedProgress, [0, 1], [0, -100])
        : interpolate(easedProgress, [0, 1], [100, 0]);
      return {
        opacity: 1,
        transform: `translateX(${translateLeft}%)`,
      };

    case 'slide-right':
      const translateRight = isOutgoing
        ? interpolate(easedProgress, [0, 1], [0, 100])
        : interpolate(easedProgress, [0, 1], [-100, 0]);
      return {
        opacity: 1,
        transform: `translateX(${translateRight}%)`,
      };

    default:
      return { opacity: 1, transform: 'none' };
  }
};
