// ============================================
// Sketch → Color 효과
// 흑백 스케치에서 점점 컬러로 변환
// ============================================
import { AbsoluteFill, useCurrentFrame, interpolate, Img, Easing } from 'remotion';

interface SketchToColorProps {
  src: string;
  durationInFrames?: number;
}

const resolveSrc = (src: string): string => {
  if (src.startsWith('/data/media/')) {
    return `http://localhost:3001${src.replace('/data/media/', '/media/')}`;
  }
  return src;
};

export const SketchToColor: React.FC<SketchToColorProps> = ({
  src,
  durationInFrames = 150,
}) => {
  const frame = useCurrentFrame();

  // Grayscale: 100% → 0%
  const grayscale = interpolate(
    frame,
    [0, durationInFrames * 0.7],
    [100, 0],
    { extrapolateRight: 'clamp', easing: Easing.out(Easing.quad) }
  );

  // Contrast: 높음 → 보통 (스케치 느낌)
  const contrast = interpolate(
    frame,
    [0, durationInFrames * 0.5],
    [150, 100],
    { extrapolateRight: 'clamp' }
  );

  // Brightness
  const brightness = interpolate(
    frame,
    [0, durationInFrames * 0.6],
    [90, 100],
    { extrapolateRight: 'clamp' }
  );

  // Sepia 톤
  const sepia = interpolate(
    frame,
    [0, durationInFrames * 0.5],
    [30, 0],
    { extrapolateRight: 'clamp' }
  );

  // 줌인 → 줌아웃 (원래 크기로 복귀)
  const scale = interpolate(
    frame,
    [0, durationInFrames * 0.5, durationInFrames],
    [1.05, 1.08, 1], // 살짝 줌인 후 원래대로
    { easing: Easing.inOut(Easing.ease) }
  );

  // 페이드인
  const opacity = interpolate(
    frame,
    [0, 15],
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ background: '#1a1a1a' }}>
      <AbsoluteFill style={{
        opacity,
        transform: `scale(${scale})`,
      }}>
        <Img
          src={resolveSrc(src)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: `grayscale(${grayscale}%) contrast(${contrast}%) brightness(${brightness}%) sepia(${sepia}%)`,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const SKETCH_TO_COLOR_DURATION = 150;
