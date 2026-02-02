-- =====================
-- Seed data: Creatures
-- =====================

-- 포유류 / Mammals
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('고양이', 'Cat', '포유류', 'Mammal'), ('강아지', 'Dog', '포유류', 'Mammal'), ('사자', 'Lion', '포유류', 'Mammal'), ('호랑이', 'Tiger', '포유류', 'Mammal'),
('코끼리', 'Elephant', '포유류', 'Mammal'), ('기린', 'Giraffe', '포유류', 'Mammal'), ('곰', 'Bear', '포유류', 'Mammal'), ('늑대', 'Wolf', '포유류', 'Mammal'),
('여우', 'Fox', '포유류', 'Mammal'), ('토끼', 'Rabbit', '포유류', 'Mammal'), ('다람쥐', 'Squirrel', '포유류', 'Mammal'), ('햄스터', 'Hamster', '포유류', 'Mammal'),
('판다', 'Panda', '포유류', 'Mammal'), ('코알라', 'Koala', '포유류', 'Mammal'), ('캥거루', 'Kangaroo', '포유류', 'Mammal'), ('하마', 'Hippo', '포유류', 'Mammal');

-- 조류 / Birds
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('펭귄', 'Penguin', '조류', 'Bird'), ('치킨', 'Chicken', '조류', 'Bird'), ('독수리', 'Eagle', '조류', 'Bird'), ('앵무새', 'Parrot', '조류', 'Bird'),
('부엉이', 'Owl', '조류', 'Bird'), ('플라밍고', 'Flamingo', '조류', 'Bird'), ('공작새', 'Peacock', '조류', 'Bird'), ('까마귀', 'Crow', '조류', 'Bird'),
('비둘기', 'Pigeon', '조류', 'Bird'), ('참새', 'Sparrow', '조류', 'Bird'), ('오리', 'Duck', '조류', 'Bird'), ('거위', 'Goose', '조류', 'Bird');

-- 해양생물 / Sea Creatures
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('상어', 'Shark', '해양생물', 'Sea Creature'), ('고래', 'Whale', '해양생물', 'Sea Creature'), ('돌고래', 'Dolphin', '해양생물', 'Sea Creature'), ('문어', 'Octopus', '해양생물', 'Sea Creature'),
('오징어', 'Squid', '해양생물', 'Sea Creature'), ('해파리', 'Jellyfish', '해양생물', 'Sea Creature'), ('거북이', 'Turtle', '해양생물', 'Sea Creature'), ('게', 'Crab', '해양생물', 'Sea Creature'),
('새우', 'Shrimp', '해양생물', 'Sea Creature'), ('불가사리', 'Starfish', '해양생물', 'Sea Creature'), ('조개', 'Clam', '해양생물', 'Sea Creature'), ('해마', 'Seahorse', '해양생물', 'Sea Creature');

-- 파충류 & 양서류 / Reptiles & Amphibians
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('공룡', 'Dinosaur', '파충류', 'Reptile'), ('악어', 'Crocodile', '파충류', 'Reptile'), ('뱀', 'Snake', '파충류', 'Reptile'), ('도마뱀', 'Lizard', '파충류', 'Reptile'),
('카멜레온', 'Chameleon', '파충류', 'Reptile'), ('이구아나', 'Iguana', '파충류', 'Reptile'), ('개구리', 'Frog', '양서류', 'Amphibian'), ('도롱뇽', 'Salamander', '양서류', 'Amphibian');

-- 곤충 / Insects
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('벌', 'Bee', '곤충', 'Insect'), ('나비', 'Butterfly', '곤충', 'Insect'), ('개미', 'Ant', '곤충', 'Insect'), ('무당벌레', 'Ladybug', '곤충', 'Insect'),
('잠자리', 'Dragonfly', '곤충', 'Insect'), ('반딧불이', 'Firefly', '곤충', 'Insect'), ('귀뚜라미', 'Cricket', '곤충', 'Insect'), ('사마귀', 'Mantis', '곤충', 'Insect');

-- 신화 생물 / Mythical Creatures
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('드래곤', 'Dragon', '신화', 'Mythical'), ('유니콘', 'Unicorn', '신화', 'Mythical'), ('불사조', 'Phoenix', '신화', 'Mythical'), ('그리핀', 'Griffin', '신화', 'Mythical'),
('페가수스', 'Pegasus', '신화', 'Mythical'), ('켄타우로스', 'Centaur', '신화', 'Mythical'), ('미노타우로스', 'Minotaur', '신화', 'Mythical'), ('키메라', 'Chimera', '신화', 'Mythical'),
('크라켄', 'Kraken', '신화', 'Mythical'), ('고블린', 'Goblin', '신화', 'Mythical'), ('트롤', 'Troll', '신화', 'Mythical'), ('오크', 'Orc', '신화', 'Mythical'),
('엘프', 'Elf', '신화', 'Mythical'), ('요정', 'Fairy', '신화', 'Mythical'), ('인어', 'Mermaid', '신화', 'Mythical'), ('늑대인간', 'Werewolf', '신화', 'Mythical');

-- 기타 / Humanoid / Misc
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('로봇', 'Robot', '기타', 'Misc'), ('외계인', 'Alien', '기타', 'Misc'), ('좀비', 'Zombie', '기타', 'Misc'), ('해골', 'Skeleton', '기타', 'Misc'),
('유령', 'Ghost', '기타', 'Misc'), ('닌자', 'Ninja', '기타', 'Misc'), ('해적', 'Pirate', '기타', 'Misc'), ('기사', 'Knight', '기타', 'Misc'),
('마법사', 'Wizard', '기타', 'Misc'), ('슈퍼히어로', 'Superhero', '기타', 'Misc'), ('거인', 'Giant', '기타', 'Misc'), ('난쟁이', 'Dwarf', '기타', 'Misc');

-- 직업 / Professions
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('소방관', 'Firefighter', '직업', 'Profession'), ('경찰관', 'Police Officer', '직업', 'Profession'), ('셰프', 'Chef', '직업', 'Profession'), ('과학자', 'Scientist', '직업', 'Profession'),
('의사', 'Doctor', '직업', 'Profession'), ('간호사', 'Nurse', '직업', 'Profession'), ('선생님', 'Teacher', '직업', 'Profession'), ('변호사', 'Lawyer', '직업', 'Profession'),
('건축가', 'Architect', '직업', 'Profession'), ('화가', 'Painter', '직업', 'Profession'), ('음악가', 'Musician', '직업', 'Profession'), ('배우', 'Actor', '직업', 'Profession'),
('운동선수', 'Athlete', '직업', 'Profession'), ('우주비행사', 'Astronaut', '직업', 'Profession'), ('탐험가', 'Explorer', '직업', 'Profession'), ('사육사', 'Zookeeper', '직업', 'Profession'),
('조종사', 'Pilot', '직업', 'Profession'), ('선장', 'Captain', '직업', 'Profession'), ('광부', 'Miner', '직업', 'Profession'), ('농부', 'Farmer', '직업', 'Profession')
ON CONFLICT (name) DO NOTHING;

-- 역사 캐릭터 / Historical Characters
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('바이킹', 'Viking', '역사', 'Historical'), ('사무라이', 'Samurai', '역사', 'Historical'), ('검투사', 'Gladiator', '역사', 'Historical'), ('스파르탄', 'Spartan', '역사', 'Historical'),
('카우보이', 'Cowboy', '역사', 'Historical'), ('전사', 'Warrior', '역사', 'Historical'), ('궁수', 'Archer', '역사', 'Historical'), ('십자군', 'Crusader', '역사', 'Historical'),
('파라오', 'Pharaoh', '역사', 'Historical'), ('황제', 'Emperor', '역사', 'Historical'), ('여왕', 'Queen', '역사', 'Historical'), ('왕자', 'Prince', '역사', 'Historical'),
('공주', 'Princess', '역사', 'Historical'), ('귀족', 'Noble', '역사', 'Historical'), ('농노', 'Serf', '역사', 'Historical'), ('대장장이', 'Blacksmith', '역사', 'Historical')
ON CONFLICT (name) DO NOTHING;

-- 추가 신화 생물 / More Mythical Creatures
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('히드라', 'Hydra', '신화', 'Mythical'), ('케르베로스', 'Cerberus', '신화', 'Mythical'), ('바실리스크', 'Basilisk', '신화', 'Mythical'), ('만티코어', 'Manticore', '신화', 'Mythical'),
('스핑크스', 'Sphinx', '신화', 'Mythical'), ('하피', 'Harpy', '신화', 'Mythical'), ('키클롭스', 'Cyclops', '신화', 'Mythical'), ('메두사', 'Medusa', '신화', 'Mythical'),
('골렘', 'Golem', '신화', 'Mythical'), ('슬라임', 'Slime', '신화', 'Mythical'), ('도깨비불', 'Wisp', '신화', 'Mythical'), ('임프', 'Imp', '신화', 'Mythical'),
('가고일', 'Gargoyle', '신화', 'Mythical'), ('뱀파이어', 'Vampire', '신화', 'Mythical'), ('미라', 'Mummy', '신화', 'Mythical'), ('프랑켄슈타인', 'Frankenstein', '신화', 'Mythical'),
('늑대인간왕', 'Werewolf King', '신화', 'Mythical'), ('예티', 'Yeti', '신화', 'Mythical'), ('빅풋', 'Bigfoot', '신화', 'Mythical'), ('네시', 'Nessie', '신화', 'Mythical')
ON CONFLICT (name) DO NOTHING;

-- 귀여운 동물 / Cute Animals
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('치와와', 'Chihuahua', '포유류', 'Mammal'), ('포메라니안', 'Pomeranian', '포유류', 'Mammal'), ('시바이누', 'Shiba Inu', '포유류', 'Mammal'), ('골든리트리버', 'Golden Retriever', '포유류', 'Mammal'),
('페르시안고양이', 'Persian Cat', '포유류', 'Mammal'), ('먼치킨고양이', 'Munchkin Cat', '포유류', 'Mammal'), ('래그돌고양이', 'Ragdoll Cat', '포유류', 'Mammal'), ('수달', 'Otter', '포유류', 'Mammal'),
('미어캣', 'Meerkat', '포유류', 'Mammal'), ('친칠라', 'Chinchilla', '포유류', 'Mammal'), ('페럿', 'Ferret', '포유류', 'Mammal'), ('고슴도치', 'Hedgehog', '포유류', 'Mammal'),
('슈가글라이더', 'Sugar Glider', '포유류', 'Mammal'), ('카피바라', 'Capybara', '포유류', 'Mammal'), ('알파카', 'Alpaca', '포유류', 'Mammal'), ('라마', 'Llama', '포유류', 'Mammal')
ON CONFLICT (name) DO NOTHING;

-- 추가 해양생물 / More Sea Creatures
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('대왕오징어', 'Giant Squid', '해양생물', 'Sea Creature'), ('흰동가리', 'Clownfish', '해양생물', 'Sea Creature'), ('해룡', 'Sea Dragon', '해양생물', 'Sea Creature'), ('만타가오리', 'Manta Ray', '해양생물', 'Sea Creature'),
('바다코끼리', 'Walrus', '해양생물', 'Sea Creature'), ('물개', 'Seal', '해양생물', 'Sea Creature'), ('황제펭귄', 'Emperor Penguin', '해양생물', 'Sea Creature'), ('바다거북', 'Sea Turtle', '해양생물', 'Sea Creature'),
('산호초', 'Coral Polyp', '해양생물', 'Sea Creature'), ('말미잘', 'Sea Anemone', '해양생물', 'Sea Creature'), ('성게', 'Sea Urchin', '해양생물', 'Sea Creature'), ('랍스터', 'Lobster', '해양생물', 'Sea Creature')
ON CONFLICT (name) DO NOTHING;

-- 공룡 / Dinosaurs
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('티라노사우루스', 'Tyrannosaurus Rex', '공룡', 'Dinosaur'), ('트리케라톱스', 'Triceratops', '공룡', 'Dinosaur'), ('브라키오사우루스', 'Brachiosaurus', '공룡', 'Dinosaur'), ('벨로키랍토르', 'Velociraptor', '공룡', 'Dinosaur'),
('스테고사우루스', 'Stegosaurus', '공룡', 'Dinosaur'), ('안킬로사우루스', 'Ankylosaurus', '공룡', 'Dinosaur'), ('프테라노돈', 'Pteranodon', '공룡', 'Dinosaur'), ('스피노사우루스', 'Spinosaurus', '공룡', 'Dinosaur'),
('파라사우롤로푸스', 'Parasaurolophus', '공룡', 'Dinosaur'), ('딜로포사우루스', 'Dilophosaurus', '공룡', 'Dinosaur'), ('이구아노돈', 'Iguanodon', '공룡', 'Dinosaur'), ('알로사우루스', 'Allosaurus', '공룡', 'Dinosaur')
ON CONFLICT (name) DO NOTHING;

-- 로봇 / AI / Robots / AI
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('안드로이드', 'Android', '기계', 'Machine'), ('사이보그', 'Cyborg', '기계', 'Machine'), ('드로이드', 'Droid', '기계', 'Machine'), ('메카', 'Mecha', '기계', 'Machine'),
('청소로봇', 'Cleaning Robot', '기계', 'Machine'), ('배달로봇', 'Delivery Robot', '기계', 'Machine'), ('의료로봇', 'Medical Robot', '기계', 'Machine'), ('군사로봇', 'Military Robot', '기계', 'Machine'),
('AI비서', 'AI Assistant', '기계', 'Machine'), ('챗봇', 'Chatbot', '기계', 'Machine'), ('자율주행차', 'Self-Driving Car', '기계', 'Machine'), ('배달드론', 'Delivery Drone', '기계', 'Machine')
ON CONFLICT (name) DO NOTHING;

-- 신화 신 / Mythology Gods
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('천사', 'Angel', '신화신', 'Mythology'), ('악마', 'Demon', '신화신', 'Mythology'), ('신', 'God', '신화신', 'Mythology'), ('여신', 'Goddess', '신화신', 'Mythology'),
('큐피드', 'Cupid', '신화신', 'Mythology'), ('제우스', 'Zeus', '신화신', 'Mythology'), ('포세이돈', 'Poseidon', '신화신', 'Mythology'), ('하데스', 'Hades', '신화신', 'Mythology'),
('아테나', 'Athena', '신화신', 'Mythology'), ('아폴로', 'Apollo', '신화신', 'Mythology'), ('토르', 'Thor', '신화신', 'Mythology'), ('오딘', 'Odin', '신화신', 'Mythology'),
('손오공', 'Sun Wukong', '신화신', 'Mythology'), ('저팔계', 'Zhu Bajie', '신화신', 'Mythology'), ('삼장법사', 'Tang Sanzang', '신화신', 'Mythology'), ('사오정', 'Sha Wujing', '신화신', 'Mythology')
ON CONFLICT (name) DO NOTHING;

-- 공포 / Horror
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('저승사자', 'Specter', '공포', 'Horror'), ('반시', 'Banshee', '공포', 'Horror'), ('도깨비왕', 'Goblin King', '공포', 'Horror'), ('구미호', 'Nine-Tailed Fox', '공포', 'Horror'),
('사신', 'Grim Reaper', '공포', 'Horror'), ('강시', 'Jiangshi', '공포', 'Horror'), ('원귀', 'Wraith', '공포', 'Horror'), ('물귀신', 'Water Spirit', '공포', 'Horror'),
('산신령', 'Mountain Spirit', '공포', 'Horror'), ('수호수', 'Guardian Beast', '공포', 'Horror'), ('철우', 'Iron Bull', '공포', 'Horror'), ('삼족오', 'Three-Legged Crow', '공포', 'Horror')
ON CONFLICT (name) DO NOTHING;

-- 게임/애니 캐릭터 / Game / Anime Character Types
INSERT INTO creatures (name, name_en, category, category_en) VALUES
('용사', 'Hero', '캐릭터', 'Character'), ('마왕', 'Demon Lord', '캐릭터', 'Character'), ('힐러', 'Healer', '캐릭터', 'Character'), ('탱커', 'Tank', '캐릭터', 'Character'),
('암살자', 'Assassin', '캐릭터', 'Character'), ('레인저', 'Ranger', '캐릭터', 'Character'), ('소환사', 'Summoner', '캐릭터', 'Character'), ('연금술사', 'Alchemist', '캐릭터', 'Character'),
('음유시인', 'Bard', '캐릭터', 'Character'), ('성기사', 'Paladin', '캐릭터', 'Character'), ('강령술사', 'Necromancer', '캐릭터', 'Character'), ('드루이드', 'Druid', '캐릭터', 'Character')
ON CONFLICT (name) DO NOTHING;

-- =====================
-- Utility Views
-- =====================

-- Random unused combination view
CREATE VIEW random_unused_combination AS
SELECT
    o.id as object_id,
    o.name as object_name,
    o.name_en as object_name_en,
    o.category as object_category,
    o.category_en as object_category_en,
    c.id as creature_id,
    c.name as creature_name,
    c.name_en as creature_name_en,
    c.category as creature_category,
    c.category_en as creature_category_en
FROM objects o
CROSS JOIN creatures c
WHERE NOT EXISTS (
    SELECT 1 FROM combinations_used cu
    WHERE cu.object_id = o.id AND cu.creature_id = c.id
)
ORDER BY RANDOM()
LIMIT 1;
