-- =============================================
-- vs_scripts table: 대결 모드 스크립트 저장
-- =============================================
CREATE TABLE vs_scripts (
    id SERIAL PRIMARY KEY,

    -- Team 1: object + creature
    team1_object_id INTEGER REFERENCES objects(id),
    team1_creature_id INTEGER REFERENCES creatures(id),
    team1_object_name VARCHAR(100),
    team1_object_name_en VARCHAR(100),
    team1_creature_name VARCHAR(100),
    team1_creature_name_en VARCHAR(100),

    -- Team 2: object + creature
    team2_object_id INTEGER REFERENCES objects(id),
    team2_creature_id INTEGER REFERENCES creatures(id),
    team2_object_name VARCHAR(100),
    team2_object_name_en VARCHAR(100),
    team2_creature_name VARCHAR(100),
    team2_creature_name_en VARCHAR(100),

    -- LLM generated result
    situations JSONB NOT NULL,

    -- Generated media URLs
    image_url TEXT,
    video_url TEXT,

    -- Status management
    status VARCHAR(20) DEFAULT 'pending',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for vs_scripts
CREATE INDEX idx_vs_scripts_status ON vs_scripts(status);
CREATE INDEX idx_vs_scripts_team1 ON vs_scripts(team1_object_id, team1_creature_id);
CREATE INDEX idx_vs_scripts_team2 ON vs_scripts(team2_object_id, team2_creature_id);
