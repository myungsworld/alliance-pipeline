-- =====================
-- Base Tables
-- =====================

-- Objects table
CREATE TABLE objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    category_en VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Creatures table
CREATE TABLE creatures (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    category_en VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Used combinations (prevent duplicates)
CREATE TABLE combinations_used (
    id SERIAL PRIMARY KEY,
    object_id INT REFERENCES objects(id),
    creature_id INT REFERENCES creatures(id),
    content_type VARCHAR(50),
    used_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(object_id, creature_id, content_type)
);

-- Indexes
CREATE INDEX idx_objects_category ON objects(category);
CREATE INDEX idx_creatures_category ON creatures(category);
