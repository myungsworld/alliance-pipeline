// ============================================
// Brush Reveal 효과
// 중앙에서 원형으로 확산되며 이미지가 드러남
// ============================================
import { AbsoluteFill, useCurrentFrame, interpolate, Img, Easing } from 'remotion';

interface BrushRevealProps {
  src: string;
  durationInFrames?: number;
}

const resolveSrc = (src: string): string => {
  if (src.startsWith('/data/media/')) {
    return `http://localhost:3001${src.replace('/data/media/', '/media/')}`;
  }
  return src;
};

export const BrushReveal: React.FC<BrushRevealProps> = ({
  src,
  durationInFrames = 150,
}) => {
  const frame = useCurrentFrame();

  // 원형 확산 크기 (0% → 150%)
  const circleSize = interpolate(
    frame,
    [0, durationInFrames * 0.85],
    [0, 150],
    { extrapolateRight: 'clamp', easing: Easing.out(Easing.quad) }
  );

  // 배경 블러 opacity
  const bgOpacity = interpolate(
    frame,
    [0, durationInFrames * 0.3],
    [0, 0.3],
    { extrapolateRight: 'clamp' }
  );

  // 마스크 그라디언트
  const maskGradient = `radial-gradient(ellipse ${circleSize}% ${circleSize * 1.5}% at 50% 50%, black ${circleSize * 0.7}%, transparent ${circleSize}%)`;

  // 마지막에 완전히 보이게 (마스크 제거)
  const showFullImage = frame > durationInFrames * 0.9;

  return (
    <AbsoluteFill style={{ background: '#0f0f0f' }}>
      {/* 배경 (블러) */}
      <Img
        src={resolveSrc(src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          opacity: bgOpacity,
          filter: 'blur(20px) brightness(0.3)',
        }}
      />

      {/* 메인 이미지 */}
      <AbsoluteFill>
        <div style={{
          width: '100%',
          height: '100%',
          WebkitMaskImage: showFullImage ? 'none' : maskGradient,
          maskImage: showFullImage ? 'none' : maskGradient,
        }}>
          <Img
            src={resolveSrc(src)}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
            }}
          />
        </div>
      </AbsoluteFill>

      {/* 빛나는 엣지 효과 */}
      {circleSize > 10 && circleSize < 140 && (
        <AbsoluteFill style={{
          background: `radial-gradient(ellipse ${circleSize}% ${circleSize * 1.5}% at 50% 50%, transparent ${circleSize * 0.6}%, rgba(255,255,255,0.2) ${circleSize * 0.7}%, transparent ${circleSize * 0.8}%)`,
          pointerEvents: 'none',
        }} />
      )}
    </AbsoluteFill>
  );
};

export const BRUSH_REVEAL_DURATION = 150;
