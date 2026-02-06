// ============================================
// 슬롯머신 메인 컴포지션
// 모든 요소를 조합하여 최종 영상 구성
// ============================================
import { AbsoluteFill, useCurrentFrame, interpolate, Easing, Audio, staticFile } from 'remotion';
import { SlotReel } from './SlotReel';
import { COLORS, TIMING, BOSS_OPTIONS, HERO_OPTIONS } from './config';
import { SlotMachineProps } from '../../types';

export const SlotMachine: React.FC<SlotMachineProps> = ({ boss, hero, seed, audioSrc, audioVolume = 1 }) => {
  const frame = useCurrentFrame();

  // 오디오 경로: public 폴더 파일은 staticFile() 사용
  const resolvedAudioSrc = audioSrc ? staticFile(audioSrc) : undefined;

  // ========== 타이밍 계산 ==========
  const bossStartFrame = 30;  // 1초 후 시작
  const heroStartFrame = bossStartFrame + TIMING.heroDelay;
  const heroEndFrame = heroStartFrame + TIMING.bossSpinDuration + TIMING.heroExtraTime;

  // ========== 애니메이션 값들 ==========
  // 타이틀 페이드인
  const titleOpacity = interpolate(frame, [0, TIMING.titleFadeIn], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const titleY = interpolate(frame, [0, TIMING.titleFadeIn], [-30, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.ease),
  });

  // 슬롯머신 페이드인
  const slotOpacity = interpolate(
    frame,
    [TIMING.slotMachineFadeIn, TIMING.slotMachineFadeIn + TIMING.titleFadeIn],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // VS 펄스 애니메이션
  const vsPulse = interpolate(
    frame % 24,  // 24프레임(0.8초) 주기
    [0, 12, 24],
    [1, 1.15, 1],
    { extrapolateRight: 'clamp' }
  );

  // 완료 후 플래시 효과
  const isComplete = frame >= heroEndFrame;
  const flashIntensity = isComplete
    ? interpolate(frame % 15, [0, 7, 15], [0.4, 0.8, 0.4])
    : 0.4;

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f1a 100%)',
      fontFamily: "'Arial Black', sans-serif",
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '40px 20px',
    }}>
      {/* 배경 오디오 (선택적) */}
      {resolvedAudioSrc && (
        <Audio src={resolvedAudioSrc} volume={audioVolume} />
      )}
      {/* 타이틀 */}
      <div style={{
        textAlign: 'center',
        marginBottom: 40,
        opacity: titleOpacity,
        transform: `translateY(${titleY}px)`,
      }}>
        <h1 style={{
          fontSize: 64,
          color: COLORS.gold,
          textShadow: `0 0 20px ${COLORS.gold}, 0 0 40px ${COLORS.gold}, 4px 4px 0 #000`,
          letterSpacing: 5,
          margin: 0,
        }}>
          EPIC BATTLE
        </h1>
        <div style={{
          color: '#888',
          fontSize: 19,
          marginTop: 10,
          letterSpacing: 3,
        }}>
          TODAY'S MATCHUP
        </div>
      </div>

      {/* 슬롯머신 */}
      <div style={{
        background: 'linear-gradient(180deg, #2a2a4a 0%, #1a1a2e 100%)',
        borderRadius: 30,
        padding: 40,
        boxShadow: `0 0 ${60 * flashIntensity}px rgba(255, 215, 0, ${flashIntensity})`,
        border: `5px solid ${COLORS.gold}`,
        opacity: slotOpacity,
      }}>
        {/* 상단 조명 */}
        <Lights frame={frame} />

        {/* 슬롯 컨테이너 */}
        <div style={{
          display: 'flex',
          gap: 30,
          justifyContent: 'center',
          alignItems: 'center',
        }}>
          {/* Boss 슬롯 */}
          <div style={{ width: 250, textAlign: 'center' }}>
            <SlotLabel type="boss" />
            <SlotReel
              items={BOSS_OPTIONS}
              finalValue={boss}
              startFrame={bossStartFrame}
              duration={TIMING.bossSpinDuration}
              type="boss"
              seed={seed}
            />
          </div>

          {/* VS */}
          <div style={{
            fontSize: 64,
            color: COLORS.gold,
            textShadow: `0 0 30px ${COLORS.gold}, 0 0 60px ${COLORS.gold}`,
            transform: `scale(${vsPulse})`,
          }}>
            VS
          </div>

          {/* Hero 슬롯 */}
          <div style={{ width: 250, textAlign: 'center' }}>
            <SlotLabel type="hero" />
            <SlotReel
              items={HERO_OPTIONS}
              finalValue={hero}
              startFrame={heroStartFrame}
              duration={TIMING.bossSpinDuration + TIMING.heroExtraTime}
              type="hero"
              seed={seed}
            />
          </div>
        </div>

        {/* 하단 조명 */}
        <div style={{ marginTop: 25 }}>
          <Lights frame={frame} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============================================
// 슬롯 라벨 컴포넌트
// ============================================
const SlotLabel: React.FC<{ type: 'boss' | 'hero' }> = ({ type }) => {
  const isBoss = type === 'boss';
  return (
    <div style={{
      fontSize: 32,
      fontWeight: 'bold',
      marginBottom: 15,
      padding: '10px 30px',
      borderRadius: 15,
      color: isBoss ? COLORS.glowBoss : COLORS.glowHero,
      background: isBoss
        ? 'linear-gradient(180deg, #4a1a1a 0%, #2a0a0a 100%)'
        : 'linear-gradient(180deg, #1a2a4a 0%, #0a1a2a 100%)',
      border: `3px solid ${isBoss ? COLORS.glowBoss : COLORS.glowHero}`,
      textShadow: `0 0 15px ${isBoss ? COLORS.glowBoss : COLORS.glowHero}`,
      boxShadow: `0 0 20px ${isBoss ? 'rgba(255,68,68,0.3)' : 'rgba(68,170,255,0.3)'}`,
    }}>
      {isBoss ? 'BOSS' : 'HERO'}
    </div>
  );
};

// ============================================
// 조명 컴포넌트 (깜빡이는 효과)
// ============================================
const Lights: React.FC<{ frame: number }> = ({ frame }) => {
  const lights = Array(7).fill(null);
  return (
    <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: 25 }}>
      {lights.map((_, i) => {
        const isOdd = i % 2 === 0;
        const blinkOffset = isOdd ? 0 : 6;  // 홀짝 번갈아 깜빡임
        const opacity = interpolate(
          (frame + blinkOffset) % 12,
          [0, 6, 12],
          [0.3, 1, 0.3]
        );
        return (
          <div
            key={i}
            style={{
              width: 15,
              height: 15,
              borderRadius: '50%',
              background: isOdd ? COLORS.red : COLORS.gold,
              boxShadow: `0 0 15px ${isOdd ? COLORS.red : COLORS.gold}`,
              opacity,
            }}
          />
        );
      })}
    </div>
  );
};
