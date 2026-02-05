// ============================================
// 슬롯머신 설정
// 타이밍, 색상, 옵션 리스트 등
// ============================================

// 색상 테마
export const COLORS = {
  gold: '#ffd700',
  darkGold: '#b8860b',
  red: '#dc143c',
  darkBg: '#1a1a2e',
  slotBg: '#0f0f1a',
  glowBoss: '#ff4444',
  glowHero: '#44aaff',
} as const;

// 타이밍 설정 (프레임 기준, 30fps)
export const TIMING = {
  titleFadeIn: 24,        // 0.8초 (타이틀 페이드인)
  slotMachineFadeIn: 9,   // 0.3초 딜레이 후 페이드인
  bossSpinDuration: 90,   // 3초 (보스 릴 회전)
  heroDelay: 15,          // 0.5초 (히어로 시작 딜레이)
  heroExtraTime: 24,      // 0.8초 (히어로 추가 회전)
  resultDelay: 6,         // 결과 표시 딜레이
} as const;

// 슬롯 옵션들 (HTML에서 가져옴)
export const BOSS_OPTIONS = [
  "Angry Mom", "Monday Morning", "Alarm Clock", "Student Loans",
  "Tax Season", "DMV Lady", "Gym Trainer", "WiFi Outage",
  "Empty Fridge", "Traffic Jam", "Boss's Email", "Dentist",
  "Credit Card Bill", "Hangover", "Zoom Meeting", "Diet Day 1",
  "Ex's Instagram", "Parking Ticket", "Spider", "Low Battery"
];

export const HERO_OPTIONS = [
  "Baby Chick", "Sleepy Cat", "Confused Dog", "Office Plant",
  "Rubber Duck", "Lazy Sloth", "Tiny Hamster", "Brave Snail",
  "Fluffy Bunny", "Tired Dad", "Coffee Cup", "Pizza Slice",
  "Couch Potato", "Bubble Tea", "Goldfish", "House Cat",
  "Burrito", "Ice Cream", "Sock Puppet", "Nap Time"
];

// 슬롯 아이템 높이 (px)
export const ITEM_HEIGHT = 50;
