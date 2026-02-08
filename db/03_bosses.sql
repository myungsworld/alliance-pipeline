-- =====================
-- Bosses table (Boss vs Hero 대결)
-- =====================
CREATE TABLE IF NOT EXISTS bosses (
    id SERIAL PRIMARY KEY,

    -- 입력값 (원본)
    input_boss VARCHAR(100) NOT NULL,
    input_hero VARCHAR(100) NOT NULL,

    -- LLM 생성 결과
    boss_name VARCHAR(100),
    hero_name VARCHAR(100),
    boss_description TEXT,
    hero_description TEXT,
    location TEXT,
    template TEXT,

    -- 생성된 미디어
    img_url TEXT,              -- 로컬 경로 (/data/media/...)
    img_url_public TEXT,       -- 공개 URL (Replicate 등 외부 API용)
    video_url TEXT,            -- 생성된 영상 URL

    -- 상태 관리
    status VARCHAR(20) DEFAULT 'pending',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_bosses_status ON bosses(status);
CREATE INDEX IF NOT EXISTS idx_bosses_input ON bosses(input_boss, input_hero);
