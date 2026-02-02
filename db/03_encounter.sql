-- =====================
-- Encounter scripts table (조우 모드)
-- =====================
CREATE TABLE encounter_scripts (
    id SERIAL PRIMARY KEY,

    -- Combination info
    object_id INTEGER REFERENCES objects(id),
    creature_id INTEGER REFERENCES creatures(id),
    object_name VARCHAR(100),
    object_name_en VARCHAR(100),
    creature_name VARCHAR(100),
    creature_name_en VARCHAR(100),

    -- LLM generated result
    character_description TEXT,  -- consistent character identity/role description
    visual_hint TEXT,  -- simple creature shape for doodle-style image (e.g., "round body, short legs, big eyes")
    situations JSONB NOT NULL,  -- [{situation_eng, situation_kor, reaction_type, caption_kor}, ...]

    -- Selection info
    selected_index INTEGER,

    -- Generated media URLs
    image_url TEXT,  -- generated image URL from Replicate
    video_url TEXT,  -- generated video URL from Replicate

    -- Status management
    -- pending: created, selected: situation chosen, approved: approved, rejected: discarded
    status VARCHAR(20) DEFAULT 'pending',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_encounter_scripts_status ON encounter_scripts(status);
CREATE INDEX idx_encounter_scripts_object_creature ON encounter_scripts(object_id, creature_id);
