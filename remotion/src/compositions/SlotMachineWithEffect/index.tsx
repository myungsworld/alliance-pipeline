// ============================================
// 슬롯머신 + 줌 아웃 효과 컴포지션
// 슬롯머신 끝난 후 카메라가 앞으로 돌진하듯 줌인 → 검은화면
// ============================================
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { SlotReel } from '../SlotMachine/SlotReel';
import { COLORS, TIMING, BOSS_OPTIONS, HERO_OPTIONS } from '../SlotMachine/config';
import { SlotMachineProps } from '../../types';

// 이펙트 타이밍 설정
const EFFECT_START = 195;  // 6.5초 (슬롯머신 끝나는 시점)
const EFFECT_DURATION = 45; // 1.5초 (줌인 + 페이드아웃)

export const SlotMachineWithEffect: React.FC<SlotMachineProps> = ({ boss, hero, seed }) => {
  const frame = useCurrentFrame();

  // ========== 슬롯머신 타이밍 (기존과 동일) ==========
  const bossStartFrame = 30;
  const heroStartFrame = bossStartFrame + TIMING.heroDelay;
  const heroEndFrame = heroStartFrame + TIMING.bossSpinDuration + TIMING.heroExtraTime;

  // ========== 기존 애니메이션 값들 ==========
  const titleOpacity = interpolate(frame, [0, TIMING.titleFadeIn], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const titleY = interpolate(frame, [0, TIMING.titleFadeIn], [-30, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.ease),
  });

  const slotOpacity = interpolate(
    frame,
    [TIMING.slotMachineFadeIn, TIMING.slotMachineFadeIn + TIMING.titleFadeIn],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const vsPulse = interpolate(
    frame % 24,
    [0, 12, 24],
    [1, 1.15, 1],
    { extrapolateRight: 'clamp' }
  );

  const isComplete = frame >= heroEndFrame;
  const flashIntensity = isComplete
    ? interpolate(frame % 15, [0, 7, 15], [0.4, 0.8, 0.4])
    : 0.4;

  // ========== 줌인 + 페이드 투 블랙 효과 ==========
  const isEffectPhase = frame >= EFFECT_START;

  // 줌인: 1 → 15 (눈앞까지 돌진하는 느낌)
  const zoomScale = interpolate(
    frame,
    [EFFECT_START, EFFECT_START + EFFECT_DURATION],
    [1, 15],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.in(Easing.cubic), // 더 급격하게 가속
    }
  );

  // 페이드 투 블랙: 줌 중반부터 빠르게 검어짐
  const blackOverlayOpacity = interpolate(
    frame,
    [EFFECT_START + EFFECT_DURATION * 0.3, EFFECT_START + EFFECT_DURATION * 0.8],
    [0, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.in(Easing.quad),
    }
  );

  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {/* 메인 콘텐츠 (줌 효과 적용) */}
      <AbsoluteFill style={{
        transform: isEffectPhase ? `scale(${zoomScale})` : 'scale(1)',
        transformOrigin: 'center center',
      }}>
        <AbsoluteFill style={{
          background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f1a 100%)',
          fontFamily: "'Arial Black', sans-serif",
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '40px 20px',
        }}>
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
            <Lights frame={frame} />

            <div style={{
              display: 'flex',
              gap: 30,
              justifyContent: 'center',
              alignItems: 'center',
            }}>
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

              <div style={{
                fontSize: 64,
                color: COLORS.gold,
                textShadow: `0 0 30px ${COLORS.gold}, 0 0 60px ${COLORS.gold}`,
                transform: `scale(${vsPulse})`,
              }}>
                VS
              </div>

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

            <div style={{ marginTop: 25 }}>
              <Lights frame={frame} />
            </div>
          </div>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* 검은색 오버레이 (페이드 투 블랙) */}
      {isEffectPhase && (
        <AbsoluteFill style={{
          background: '#000',
          opacity: blackOverlayOpacity,
        }} />
      )}
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
// 조명 컴포넌트
// ============================================
const Lights: React.FC<{ frame: number }> = ({ frame }) => {
  const lights = Array(7).fill(null);
  return (
    <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: 25 }}>
      {lights.map((_, i) => {
        const isOdd = i % 2 === 0;
        const blinkOffset = isOdd ? 0 : 6;
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

// 총 duration: 195 (슬롯) + 45 (이펙트) = 240 프레임 (8초)
export const SLOT_MACHINE_WITH_EFFECT_DURATION = EFFECT_START + EFFECT_DURATION;
