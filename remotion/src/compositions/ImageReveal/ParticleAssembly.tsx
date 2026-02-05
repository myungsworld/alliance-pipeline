// ============================================
// Particle Assembly 효과
// 픽셀/파티클이 모여서 이미지가 완성됨
// ============================================
import { AbsoluteFill, useCurrentFrame, interpolate, Img, Easing } from 'remotion';
import { useMemo } from 'react';

interface ParticleAssemblyProps {
  src: string;
  durationInFrames?: number;
  gridSize?: number;
}

const resolveSrc = (src: string): string => {
  if (src.startsWith('/data/media/')) {
    return `http://localhost:3001${src.replace('/data/media/', '/media/')}`;
  }
  return src;
};

const seededRandom = (seed: number) => {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
};

export const ParticleAssembly: React.FC<ParticleAssemblyProps> = ({
  src,
  durationInFrames = 150,
  gridSize = 12,
}) => {
  const frame = useCurrentFrame();

  // 각 셀의 등장 순서
  const cells = useMemo(() => {
    const result = [];
    for (let y = 0; y < gridSize; y++) {
      for (let x = 0; x < gridSize; x++) {
        const index = y * gridSize + x;
        const appearOrder = seededRandom(index * 137 + 42);
        result.push({ x, y, appearOrder });
      }
    }
    return result;
  }, [gridSize]);

  // 전체 진행도
  const progress = interpolate(
    frame,
    [0, durationInFrames * 0.8],
    [0, 1],
    { extrapolateRight: 'clamp', easing: Easing.out(Easing.quad) }
  );

  // 마지막에 원본 이미지 페이드인 (깔끔하게 마무리)
  const finalImageOpacity = interpolate(
    frame,
    [durationInFrames * 0.75, durationInFrames * 0.95],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const cellSize = 100 / gridSize;

  return (
    <AbsoluteFill style={{ background: '#0a0a0a' }}>
      {/* 파티클 그리드 */}
      <AbsoluteFill>
        {cells.map(({ x, y, appearOrder }) => {
          const cellProgress = interpolate(
            progress,
            [appearOrder * 0.5, appearOrder * 0.5 + 0.5],
            [0, 1],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          );

          const opacity = cellProgress;
          const cellScale = interpolate(cellProgress, [0, 1], [0.8, 1]);

          return (
            <div
              key={`${x}-${y}`}
              style={{
                position: 'absolute',
                left: `${x * cellSize}%`,
                top: `${y * cellSize}%`,
                width: `${cellSize}%`,
                height: `${cellSize}%`,
                opacity,
                transform: `scale(${cellScale})`,
                overflow: 'hidden',
              }}
            >
              {/* 배경 이미지를 올바른 위치에 표시 */}
              <div style={{
                position: 'absolute',
                width: `${gridSize * 100}%`,
                height: `${gridSize * 100}%`,
                left: `${-x * 100}%`,
                top: `${-y * 100}%`,
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
            </div>
          );
        })}
      </AbsoluteFill>

      {/* 마지막에 원본 이미지로 덮어서 깔끔하게 */}
      <AbsoluteFill style={{ opacity: finalImageOpacity }}>
        <Img
          src={resolveSrc(src)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const PARTICLE_ASSEMBLY_DURATION = 150;
