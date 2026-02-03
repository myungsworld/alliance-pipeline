-- =====================
-- Bosses table schema
-- =====================
CREATE TABLE IF NOT EXISTS bosses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    category_en VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_bosses_category ON bosses(category);

-- =====================
-- Seed data: Bosses
-- =====================

-- 언데드 보스 / Undead Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('고대 리치왕', 'Ancient Lich King', '언데드 보스', 'Undead Boss'),
('죽음의 기사단장', 'Death Knight Overlord', '언데드 보스', 'Undead Boss'),
('해골 황제', 'Skeletal Emperor', '언데드 보스', 'Undead Boss'),
('영혼 포식자', 'Soul Devourer', '언데드 보스', 'Undead Boss'),
('저주받은 파라오', 'Cursed Pharaoh', '언데드 보스', 'Undead Boss'),
('뼈의 군주', 'Bone Sovereign', '언데드 보스', 'Undead Boss'),
('망령 대공', 'Wraith Archduke', '언데드 보스', 'Undead Boss'),
('역병의 왕', 'Plague King', '언데드 보스', 'Undead Boss'),
('지옥의 사령관', 'Infernal Necrolord', '언데드 보스', 'Undead Boss'),
('영원의 흡혈군주', 'Eternal Vampire Lord', '언데드 보스', 'Undead Boss')
ON CONFLICT (name) DO NOTHING;

-- 드래곤 보스 / Dragon Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('고대 흑룡', 'Ancient Black Dragon', '드래곤 보스', 'Dragon Boss'),
('세계멸망의 적룡', 'World-Ender Red Dragon', '드래곤 보스', 'Dragon Boss'),
('심연의 해룡', 'Abyssal Sea Dragon', '드래곤 보스', 'Dragon Boss'),
('시간의 용왕', 'Temporal Dragon King', '드래곤 보스', 'Dragon Boss'),
('혼돈의 용신', 'Chaos Dragon God', '드래곤 보스', 'Dragon Boss'),
('뼈의 드래곤로드', 'Bone Dragon Lord', '드래곤 보스', 'Dragon Boss'),
('암흑룡 니드호그', 'Nidhogg the Shadow Dragon', '드래곤 보스', 'Dragon Boss'),
('천둥의 뇌룡', 'Thunderstorm Lightning Dragon', '드래곤 보스', 'Dragon Boss'),
('독의 비룡', 'Venomous Wyvern King', '드래곤 보스', 'Dragon Boss'),
('황금룡 황제', 'Golden Dragon Emperor', '드래곤 보스', 'Dragon Boss'),
('얼음 서리룡', 'Frost Wyrm Sovereign', '드래곤 보스', 'Dragon Boss'),
('용암 화염룡', 'Magma Fire Dragon', '드래곤 보스', 'Dragon Boss')
ON CONFLICT (name) DO NOTHING;

-- 악마 보스 / Demon Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('지옥의 대군주', 'Archdemon Overlord', '악마 보스', 'Demon Boss'),
('일곱 죄악의 왕', 'King of Seven Sins', '악마 보스', 'Demon Boss'),
('타락천사 루시퍼', 'Lucifer the Fallen', '악마 보스', 'Demon Boss'),
('심연의 악마공', 'Abyssal Demon Prince', '악마 보스', 'Demon Boss'),
('지옥불 군주', 'Hellfire Monarch', '악마 보스', 'Demon Boss'),
('탐욕의 마왕', 'Demon Lord of Greed', '악마 보스', 'Demon Boss'),
('분노의 마신', 'Rage Demon God', '악마 보스', 'Demon Boss'),
('나락의 지배자', 'Ruler of the Pit', '악마 보스', 'Demon Boss'),
('혼돈의 발록', 'Chaos Balrog', '악마 보스', 'Demon Boss'),
('암흑 서큐버스 여왕', 'Dark Succubus Queen', '악마 보스', 'Demon Boss'),
('지옥견 케르베로스', 'Cerberus the Hellhound', '악마 보스', 'Demon Boss'),
('악마왕 벨제부브', 'Beelzebub the Demon King', '악마 보스', 'Demon Boss')
ON CONFLICT (name) DO NOTHING;

-- 엘리멘탈 보스 / Elemental Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('태초의 화염왕', 'Primordial Fire King', '엘리멘탈 보스', 'Elemental Boss'),
('심해의 해신', 'Abyssal Sea God', '엘리멘탈 보스', 'Elemental Boss'),
('폭풍의 군주', 'Storm Sovereign', '엘리멘탈 보스', 'Elemental Boss'),
('대지의 거신', 'Earth Colossus', '엘리멘탈 보스', 'Elemental Boss'),
('얼음 빙제', 'Frost Emperor', '엘리멘탈 보스', 'Elemental Boss'),
('번개의 뇌신', 'Thunder God', '엘리멘탈 보스', 'Elemental Boss'),
('용암 거인왕', 'Magma Giant King', '엘리멘탈 보스', 'Elemental Boss'),
('허공의 지배자', 'Void Dominator', '엘리멘탈 보스', 'Elemental Boss'),
('빛의 대천사', 'Archangel of Light', '엘리멘탈 보스', 'Elemental Boss'),
('어둠의 심연왕', 'Shadow Abyss King', '엘리멘탈 보스', 'Elemental Boss')
ON CONFLICT (name) DO NOTHING;

-- 타이탄/거신 보스 / Titan Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('세계수호자 타이탄', 'World Guardian Titan', '타이탄 보스', 'Titan Boss'),
('하늘을 떠받치는 자', 'Atlas the Sky Bearer', '타이탄 보스', 'Titan Boss'),
('시간의 크로노스', 'Kronos the Time Titan', '타이탄 보스', 'Titan Boss'),
('대양의 오케아노스', 'Oceanus the Sea Titan', '타이탄 보스', 'Titan Boss'),
('태양의 히페리온', 'Hyperion the Sun Titan', '타이탄 보스', 'Titan Boss'),
('산을 움직이는 자', 'Mountain Mover Titan', '타이탄 보스', 'Titan Boss'),
('별을 삼키는 자', 'Star Swallower', '타이탄 보스', 'Titan Boss'),
('천벌의 거인', 'Divine Punishment Giant', '타이탄 보스', 'Titan Boss'),
('종말의 거신', 'Apocalypse Colossus', '타이탄 보스', 'Titan Boss'),
('창조의 원초거인', 'Primordial Creation Giant', '타이탄 보스', 'Titan Boss')
ON CONFLICT (name) DO NOTHING;

-- 크툴루/우주적 공포 보스 / Cosmic Horror Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('심연의 크툴루', 'Cthulhu of the Deep', '우주적 공포', 'Cosmic Horror'),
('혼돈의 아자토스', 'Azathoth the Chaos', '우주적 공포', 'Cosmic Horror'),
('천 개의 눈', 'Thousand-Eyed One', '우주적 공포', 'Cosmic Horror'),
('차원의 포식자', 'Dimension Devourer', '우주적 공포', 'Cosmic Horror'),
('형언할 수 없는 자', 'The Unspeakable One', '우주적 공포', 'Cosmic Horror'),
('어둠 너머의 존재', 'Being Beyond Darkness', '우주적 공포', 'Cosmic Horror'),
('별의 파괴자', 'Star Destroyer', '우주적 공포', 'Cosmic Horror'),
('공허의 심판자', 'Void Arbiter', '우주적 공포', 'Cosmic Horror'),
('은하를 삼키는 자', 'Galaxy Devourer', '우주적 공포', 'Cosmic Horror'),
('이계의 지배자', 'Otherworld Dominator', '우주적 공포', 'Cosmic Horror')
ON CONFLICT (name) DO NOTHING;

-- 기계/골렘 보스 / Construct Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('고대 전쟁병기', 'Ancient War Machine', '기계 보스', 'Construct Boss'),
('강철 거신', 'Iron Colossus', '기계 보스', 'Construct Boss'),
('마법 골렘왕', 'Arcane Golem King', '기계 보스', 'Construct Boss'),
('클락워크 황제', 'Clockwork Emperor', '기계 보스', 'Construct Boss'),
('수호자 오토마톤', 'Guardian Automaton', '기계 보스', 'Construct Boss'),
('룬 타이탄', 'Rune Titan', '기계 보스', 'Construct Boss'),
('크리스탈 거인', 'Crystal Giant', '기계 보스', 'Construct Boss'),
('마력로 수호자', 'Mana Core Guardian', '기계 보스', 'Construct Boss'),
('고대 드워프의 걸작', 'Ancient Dwarven Masterwork', '기계 보스', 'Construct Boss'),
('기계신 오토마타', 'Machine God Automata', '기계 보스', 'Construct Boss')
ON CONFLICT (name) DO NOTHING;

-- 자연재해 보스 / Calamity Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('화산의 심장', 'Heart of the Volcano', '재해 보스', 'Calamity Boss'),
('대해일의 군주', 'Tsunami Overlord', '재해 보스', 'Calamity Boss'),
('지진의 원흉', 'Earthquake Harbinger', '재해 보스', 'Calamity Boss'),
('토네이도 군주', 'Tornado Lord', '재해 보스', 'Calamity Boss'),
('블리자드의 화신', 'Blizzard Incarnate', '재해 보스', 'Calamity Boss'),
('역병의 화신', 'Plague Incarnate', '재해 보스', 'Calamity Boss'),
('기근의 기수', 'Famine Horseman', '재해 보스', 'Calamity Boss'),
('전쟁의 화신', 'War Incarnate', '재해 보스', 'Calamity Boss'),
('죽음의 기수', 'Death Horseman', '재해 보스', 'Calamity Boss'),
('세계종말의 전조', 'Harbinger of Apocalypse', '재해 보스', 'Calamity Boss')
ON CONFLICT (name) DO NOTHING;

-- 몬스터 군주 보스 / Monster Lord Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('오크 대군주', 'Orc Supreme Warlord', '군주 보스', 'Monster Lord Boss'),
('트롤 대왕', 'Troll High King', '군주 보스', 'Monster Lord Boss'),
('오우거 타이탄', 'Ogre Titan', '군주 보스', 'Monster Lord Boss'),
('고블린 대제왕', 'Goblin Emperor', '군주 보스', 'Monster Lord Boss'),
('코볼트 신관왕', 'Kobold High Priest King', '군주 보스', 'Monster Lord Boss'),
('노움 기계왕', 'Gnome Machine King', '군주 보스', 'Monster Lord Boss'),
('하피 여왕', 'Harpy Queen', '군주 보스', 'Monster Lord Boss'),
('메두사 여제', 'Medusa Empress', '군주 보스', 'Monster Lord Boss'),
('미노타우로스 대장군', 'Minotaur Grand General', '군주 보스', 'Monster Lord Boss'),
('켄타우로스 대군주', 'Centaur Warlord', '군주 보스', 'Monster Lord Boss'),
('라미아 여왕', 'Lamia Queen', '군주 보스', 'Monster Lord Boss'),
('사이클롭스 대장', 'Cyclops Chieftain', '군주 보스', 'Monster Lord Boss')
ON CONFLICT (name) DO NOTHING;

-- 신화 보스 / Mythical Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('세계뱀 요르문간드', 'Jormungandr World Serpent', '신화 보스', 'Mythical Boss'),
('지옥늑대 펜리르', 'Fenrir the Hell Wolf', '신화 보스', 'Mythical Boss'),
('히드라 황제', 'Hydra Emperor', '신화 보스', 'Mythical Boss'),
('스핑크스 대현자', 'Sphinx Grand Sage', '신화 보스', 'Mythical Boss'),
('그리폰 수호왕', 'Griffin Guardian King', '신화 보스', 'Mythical Boss'),
('바실리스크 대왕', 'Basilisk High King', '신화 보스', 'Mythical Boss'),
('만티코어 군주', 'Manticore Lord', '신화 보스', 'Mythical Boss'),
('키메라 대제', 'Chimera Archon', '신화 보스', 'Mythical Boss'),
('크라켄 심해왕', 'Kraken Deep Sea King', '신화 보스', 'Mythical Boss'),
('레비아탄', 'Leviathan', '신화 보스', 'Mythical Boss'),
('베히모스', 'Behemoth', '신화 보스', 'Mythical Boss'),
('지즈 천공왕', 'Ziz Sky King', '신화 보스', 'Mythical Boss')
ON CONFLICT (name) DO NOTHING;

-- 어둠 군주 보스 / Dark Lord Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('어둠의 황제', 'Dark Emperor', '어둠 군주', 'Dark Lord Boss'),
('그림자 대공', 'Shadow Archduke', '어둠 군주', 'Dark Lord Boss'),
('암흑 마법사왕', 'Dark Sorcerer King', '어둠 군주', 'Dark Lord Boss'),
('타락한 성기사', 'Corrupted Holy Knight', '어둠 군주', 'Dark Lord Boss'),
('배신자 대천사', 'Betrayer Archangel', '어둠 군주', 'Dark Lord Boss'),
('저주받은 왕', 'Cursed King', '어둠 군주', 'Dark Lord Boss'),
('공포의 군주', 'Terror Lord', '어둠 군주', 'Dark Lord Boss'),
('절망의 화신', 'Despair Incarnate', '어둠 군주', 'Dark Lord Boss'),
('광기의 지배자', 'Madness Dominator', '어둠 군주', 'Dark Lord Boss'),
('종말을 부르는 자', 'The End Bringer', '어둠 군주', 'Dark Lord Boss')
ON CONFLICT (name) DO NOTHING;

-- 천상 보스 / Celestial Bosses
INSERT INTO bosses (name, name_en, category, category_en) VALUES
('타락한 세라핌', 'Fallen Seraphim', '천상 보스', 'Celestial Boss'),
('심판의 대천사', 'Archangel of Judgment', '천상 보스', 'Celestial Boss'),
('천벌의 사자', 'Divine Punishment Herald', '천상 보스', 'Celestial Boss'),
('별의 수호자', 'Star Guardian', '천상 보스', 'Celestial Boss'),
('달의 여신', 'Moon Goddess', '천상 보스', 'Celestial Boss'),
('태양신 라', 'Ra the Sun God', '천상 보스', 'Celestial Boss'),
('운명의 직조자', 'Fate Weaver', '천상 보스', 'Celestial Boss'),
('시간의 관리자', 'Time Keeper', '천상 보스', 'Celestial Boss'),
('우주의 심판관', 'Cosmic Judge', '천상 보스', 'Celestial Boss'),
('창조신의 그림자', 'Shadow of the Creator', '천상 보스', 'Celestial Boss')
ON CONFLICT (name) DO NOTHING;
