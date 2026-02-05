// ============================================
// 슬롯 릴 컴포넌트
// 회전하는 슬롯 애니메이션을 담당
// ============================================
import { useMemo } from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { ITEM_HEIGHT, COLORS } from './config';

interface SlotReelProps {
  items: string[];           // 릴에 표시할 아이템들
  finalValue: string;        // 최종 멈출 값
  startFrame: number;        // 애니메이션 시작 프레임
  duration: number;          // 회전 지속 프레임
  type: 'boss' | 'hero';     // 스타일 구분
}

// 시드 기반 랜덤 셔플 함수
const seededShuffle = (array: string[], seed: number): string[] => {
  const result = [...array];
  let currentSeed = seed;

  // 간단한 시드 랜덤 생성기
  const random = () => {
    currentSeed = (currentSeed * 9301 + 49297) % 233280;
    return currentSeed / 233280;
  };

  // Fisher-Yates 셔플
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }

  return result;
};

// 문자열에서 시드 숫자 생성
const stringToSeed = (str: string): number => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash);
};

export const SlotReel: React.FC<SlotReelProps> = ({
  items,
  finalValue,
  startFrame,
  duration,
  type,
}) => {
  const frame = useCurrentFrame();

  // 릴 아이템들 생성 (랜덤 셔플 + 최종값)
  // useMemo로 매 프레임마다 다시 셔플되지 않도록 함
  const reelItems = useMemo(() => {
    const seed = stringToSeed(finalValue + type);
    const shuffled1 = seededShuffle(items, seed);
    const shuffled2 = seededShuffle(items, seed + 1);
    const shuffled3 = seededShuffle(items, seed + 2);
    return [...shuffled1, ...shuffled2, ...shuffled3, finalValue];
  }, [items, finalValue, type]);

  const finalIndex = reelItems.length - 1;

  // 애니메이션 진행도 (0 ~ 1)
  const progress = interpolate(
    frame,
    [startFrame, startFrame + duration],
    [0, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.bezier(0.22, 1, 0.36, 1), // easeOutQuint
    }
  );

  // 현재 Y 위치 계산
  const totalDistance = finalIndex * ITEM_HEIGHT;
  const currentY = -progress * totalDistance + (ITEM_HEIGHT / 2);

  // 애니메이션 완료 여부
  const isComplete = frame >= startFrame + duration;

  return (
    <div style={{
      height: 100,
      overflow: 'hidden',
      background: COLORS.slotBg,
      borderRadius: 15,
      border: `4px solid ${isComplete ? COLORS.gold : '#444'}`,
      position: 'relative',
      boxShadow: isComplete
        ? `inset 0 0 30px rgba(0,0,0,0.9), 0 0 30px rgba(255,215,0,0.5)`
        : 'inset 0 0 30px rgba(0,0,0,0.9)',
    }}>
      {/* 릴 컨테이너 */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        transform: `translateY(${currentY}px)`,
      }}>
        {reelItems.map((item, idx) => (
          <div
            key={idx}
            style={{
              height: ITEM_HEIGHT,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: isComplete && idx === finalIndex ? 24 : 20,
              color: isComplete && idx === finalIndex ? COLORS.gold : '#fff',
              textShadow: isComplete && idx === finalIndex
                ? `0 0 15px ${COLORS.gold}`
                : '0 0 8px rgba(255,255,255,0.5)',
              whiteSpace: 'nowrap',
              padding: '0 15px',
            }}
          >
            {item}
          </div>
        ))}
      </div>

      {/* 상단 그라데이션 오버레이 */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: 25,
        background: `linear-gradient(to bottom, ${COLORS.slotBg}, transparent)`,
        pointerEvents: 'none',
      }} />

      {/* 하단 그라데이션 오버레이 */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 25,
        background: `linear-gradient(to top, ${COLORS.slotBg}, transparent)`,
        pointerEvents: 'none',
      }} />
    </div>
  );
};
