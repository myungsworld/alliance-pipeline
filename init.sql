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

-- =====================
-- Seed data: Objects
-- =====================

-- 도구 / Tools
INSERT INTO objects (name, name_en, category, category_en) VALUES
('망치', 'Hammer', '도구', 'Tool'), ('칼', 'Knife', '도구', 'Tool'), ('우산', 'Umbrella', '도구', 'Tool'), ('가위', 'Scissors', '도구', 'Tool'),
('열쇠', 'Key', '도구', 'Tool'), ('손전등', 'Flashlight', '도구', 'Tool'), ('망원경', 'Telescope', '도구', 'Tool'), ('돋보기', 'Magnifying Glass', '도구', 'Tool'),
('낚싯대', 'Fishing Rod', '도구', 'Tool'), ('삽', 'Shovel', '도구', 'Tool'), ('톱', 'Saw', '도구', 'Tool'), ('펜치', 'Pliers', '도구', 'Tool');

-- 가전제품 / Appliances
INSERT INTO objects (name, name_en, category, category_en) VALUES
('에어컨', 'Air Conditioner', '가전제품', 'Appliance'), ('냉장고', 'Refrigerator', '가전제품', 'Appliance'), ('TV', 'TV', '가전제품', 'Appliance'), ('세탁기', 'Washing Machine', '가전제품', 'Appliance'),
('전자레인지', 'Microwave', '가전제품', 'Appliance'), ('청소기', 'Vacuum Cleaner', '가전제품', 'Appliance'), ('선풍기', 'Fan', '가전제품', 'Appliance'), ('토스터', 'Toaster', '가전제품', 'Appliance'),
('믹서기', 'Blender', '가전제품', 'Appliance'), ('다리미', 'Iron', '가전제품', 'Appliance'), ('헤어드라이어', 'Hair Dryer', '가전제품', 'Appliance'), ('밥솥', 'Rice Cooker', '가전제품', 'Appliance');

-- 탈것 / Vehicles
INSERT INTO objects (name, name_en, category, category_en) VALUES
('자동차', 'Car', '탈것', 'Vehicle'), ('비행기', 'Airplane', '탈것', 'Vehicle'), ('로켓', 'Rocket', '탈것', 'Vehicle'), ('자전거', 'Bicycle', '탈것', 'Vehicle'),
('오토바이', 'Motorcycle', '탈것', 'Vehicle'), ('헬리콥터', 'Helicopter', '탈것', 'Vehicle'), ('잠수함', 'Submarine', '탈것', 'Vehicle'), ('요트', 'Yacht', '탈것', 'Vehicle'),
('스케이트보드', 'Skateboard', '탈것', 'Vehicle'), ('썰매', 'Sled', '탈것', 'Vehicle'), ('열기구', 'Hot Air Balloon', '탈것', 'Vehicle'), ('제트스키', 'Jet Ski', '탈것', 'Vehicle');

-- 악기 / Instruments
INSERT INTO objects (name, name_en, category, category_en) VALUES
('피아노', 'Piano', '악기', 'Instrument'), ('기타', 'Guitar', '악기', 'Instrument'), ('드럼', 'Drum', '악기', 'Instrument'), ('바이올린', 'Violin', '악기', 'Instrument'),
('트럼펫', 'Trumpet', '악기', 'Instrument'), ('플루트', 'Flute', '악기', 'Instrument'), ('하프', 'Harp', '악기', 'Instrument'), ('색소폰', 'Saxophone', '악기', 'Instrument'),
('아코디언', 'Accordion', '악기', 'Instrument'), ('탬버린', 'Tambourine', '악기', 'Instrument'), ('실로폰', 'Xylophone', '악기', 'Instrument'), ('우쿨렐레', 'Ukulele', '악기', 'Instrument');

-- 무기 / Weapons
INSERT INTO objects (name, name_en, category, category_en) VALUES
('검', 'Sword', '무기', 'Weapon'), ('방패', 'Shield', '무기', 'Weapon'), ('활', 'Bow', '무기', 'Weapon'), ('창', 'Spear', '무기', 'Weapon'),
('도끼', 'Axe', '무기', 'Weapon'), ('석궁', 'Crossbow', '무기', 'Weapon'), ('삼지창', 'Trident', '무기', 'Weapon'), ('철퇴', 'Mace', '무기', 'Weapon'),
('부메랑', 'Boomerang', '무기', 'Weapon'), ('수리검', 'Shuriken', '무기', 'Weapon'), ('쌍절곤', 'Nunchaku', '무기', 'Weapon'), ('채찍', 'Whip', '무기', 'Weapon');

-- 생활용품 / Everyday Items
INSERT INTO objects (name, name_en, category, category_en) VALUES
('컵', 'Cup', '생활용품', 'Everyday'), ('스마트폰', 'Smartphone', '생활용품', 'Everyday'), ('책', 'Book', '생활용품', 'Everyday'), ('신발', 'Shoes', '생활용품', 'Everyday'),
('안경', 'Glasses', '생활용품', 'Everyday'), ('시계', 'Watch', '생활용품', 'Everyday'), ('지갑', 'Wallet', '생활용품', 'Everyday'), ('가방', 'Bag', '생활용품', 'Everyday'),
('모자', 'Hat', '생활용품', 'Everyday'), ('장갑', 'Gloves', '생활용품', 'Everyday'), ('목도리', 'Scarf', '생활용품', 'Everyday'), ('양말', 'Socks', '생활용품', 'Everyday');

-- 가구 / Furniture
INSERT INTO objects (name, name_en, category, category_en) VALUES
('의자', 'Chair', '가구', 'Furniture'), ('책상', 'Desk', '가구', 'Furniture'), ('침대', 'Bed', '가구', 'Furniture'), ('소파', 'Sofa', '가구', 'Furniture'),
('옷장', 'Wardrobe', '가구', 'Furniture'), ('책장', 'Bookshelf', '가구', 'Furniture'), ('식탁', 'Dining Table', '가구', 'Furniture'), ('서랍장', 'Drawer', '가구', 'Furniture'),
('거울', 'Mirror', '가구', 'Furniture'), ('화장대', 'Vanity', '가구', 'Furniture'), ('신발장', 'Shoe Rack', '가구', 'Furniture'), ('옷걸이', 'Hanger', '가구', 'Furniture');

-- 스포츠 / Sports
INSERT INTO objects (name, name_en, category, category_en) VALUES
('축구공', 'Soccer Ball', '스포츠', 'Sports'), ('야구방망이', 'Baseball Bat', '스포츠', 'Sports'), ('테니스라켓', 'Tennis Racket', '스포츠', 'Sports'), ('골프채', 'Golf Club', '스포츠', 'Sports'),
('농구공', 'Basketball', '스포츠', 'Sports'), ('배드민턴라켓', 'Badminton Racket', '스포츠', 'Sports'), ('스키', 'Ski', '스포츠', 'Sports'), ('스노보드', 'Snowboard', '스포츠', 'Sports'),
('권투글러브', 'Boxing Gloves', '스포츠', 'Sports'), ('볼링공', 'Bowling Ball', '스포츠', 'Sports'), ('다트', 'Dart', '스포츠', 'Sports'), ('탁구채', 'Ping Pong Paddle', '스포츠', 'Sports');

-- 음식 / Food
INSERT INTO objects (name, name_en, category, category_en) VALUES
('피자', 'Pizza', '음식', 'Food'), ('햄버거', 'Hamburger', '음식', 'Food'), ('김치', 'Kimchi', '음식', 'Food'), ('초밥', 'Sushi', '음식', 'Food'),
('타코', 'Taco', '음식', 'Food'), ('파스타', 'Pasta', '음식', 'Food'), ('치킨', 'Fried Chicken', '음식', 'Food'), ('스테이크', 'Steak', '음식', 'Food'),
('라면', 'Ramen', '음식', 'Food'), ('떡볶이', 'Tteokbokki', '음식', 'Food'), ('아이스크림', 'Ice Cream', '음식', 'Food'), ('케이크', 'Cake', '음식', 'Food'),
('도넛', 'Donut', '음식', 'Food'), ('샌드위치', 'Sandwich', '음식', 'Food'), ('핫도그', 'Hot Dog', '음식', 'Food'), ('감자튀김', 'French Fries', '음식', 'Food')
ON CONFLICT (name) DO NOTHING;

-- 건물 / Buildings
INSERT INTO objects (name, name_en, category, category_en) VALUES
('성', 'Castle', '건물', 'Building'), ('피라미드', 'Pyramid', '건물', 'Building'), ('등대', 'Lighthouse', '건물', 'Building'), ('풍차', 'Windmill', '건물', 'Building'),
('탑', 'Tower', '건물', 'Building'), ('다리', 'Bridge', '건물', 'Building'), ('댐', 'Dam', '건물', 'Building'), ('터널', 'Tunnel', '건물', 'Building'),
('정글짐', 'Jungle Gym', '건물', 'Building'), ('미끄럼틀', 'Slide', '건물', 'Building'), ('관람차', 'Ferris Wheel', '건물', 'Building'), ('롤러코스터', 'Roller Coaster', '건물', 'Building'),
('텐트', 'Tent', '건물', 'Building'), ('이글루', 'Igloo', '건물', 'Building'), ('나무집', 'Treehouse', '건물', 'Building'), ('벙커', 'Bunker', '건물', 'Building')
ON CONFLICT (name) DO NOTHING;

-- 자연 / Nature
INSERT INTO objects (name, name_en, category, category_en) VALUES
('바위', 'Rock', '자연', 'Nature'), ('나무', 'Tree', '자연', 'Nature'), ('구름', 'Cloud', '자연', 'Nature'), ('번개', 'Lightning', '자연', 'Nature'),
('무지개', 'Rainbow', '자연', 'Nature'), ('폭포', 'Waterfall', '자연', 'Nature'), ('화산', 'Volcano', '자연', 'Nature'), ('빙하', 'Glacier', '자연', 'Nature'),
('모래', 'Sand', '자연', 'Nature'), ('진흙', 'Mud', '자연', 'Nature'), ('이끼', 'Moss', '자연', 'Nature'), ('산호', 'Coral', '자연', 'Nature'),
('조개껍데기', 'Seashell', '자연', 'Nature'), ('깃털', 'Feather', '자연', 'Nature'), ('뿔', 'Horn', '자연', 'Nature'), ('상어이빨', 'Shark Tooth', '자연', 'Nature')
ON CONFLICT (name) DO NOTHING;

-- SF / Sci-Fi
INSERT INTO objects (name, name_en, category, category_en) VALUES
('광선검', 'Lightsaber', 'SF', 'Sci-Fi'), ('타임머신', 'Time Machine', 'SF', 'Sci-Fi'), ('텔레포터', 'Teleporter', 'SF', 'Sci-Fi'), ('홀로그램', 'Hologram', 'SF', 'Sci-Fi'),
('로봇팔', 'Robot Arm', 'SF', 'Sci-Fi'), ('제트팩', 'Jetpack', 'SF', 'Sci-Fi'), ('레이저총', 'Laser Gun', 'SF', 'Sci-Fi'), ('방어막', 'Force Field', 'SF', 'Sci-Fi'),
('우주복', 'Space Suit', 'SF', 'Sci-Fi'), ('냉동캡슐', 'Cryo Pod', 'SF', 'Sci-Fi'), ('복제기', 'Cloning Machine', 'SF', 'Sci-Fi'), ('무중력부츠', 'Anti-Gravity Boots', 'SF', 'Sci-Fi'),
('나노봇', 'Nanobot', 'SF', 'Sci-Fi'), ('사이버눈', 'Cyber Eye', 'SF', 'Sci-Fi'), ('두뇌칩', 'Brain Chip', 'SF', 'Sci-Fi'), ('플라즈마포', 'Plasma Cannon', 'SF', 'Sci-Fi')
ON CONFLICT (name) DO NOTHING;

-- 판타지 / Fantasy
INSERT INTO objects (name, name_en, category, category_en) VALUES
('마법지팡이', 'Magic Wand', '판타지', 'Fantasy'), ('수정구슬', 'Crystal Ball', '판타지', 'Fantasy'), ('마법책', 'Spell Book', '판타지', 'Fantasy'), ('물약', 'Potion', '판타지', 'Fantasy'),
('마법양탄자', 'Magic Carpet', '판타지', 'Fantasy'), ('투명망토', 'Invisibility Cloak', '판타지', 'Fantasy'), ('요술램프', 'Genie Lamp', '판타지', 'Fantasy'), ('마법거울', 'Magic Mirror', '판타지', 'Fantasy'),
('부두인형', 'Voodoo Doll', '판타지', 'Fantasy'), ('봉인석', 'Seal Stone', '판타지', 'Fantasy'), ('소환진', 'Summoning Circle', '판타지', 'Fantasy'), ('룬', 'Rune', '판타지', 'Fantasy'),
('성배', 'Holy Grail', '판타지', 'Fantasy'), ('엑스칼리버', 'Excalibur', '판타지', 'Fantasy'), ('힘의반지', 'Ring of Power', '판타지', 'Fantasy'), ('왕관', 'Crown', '판타지', 'Fantasy')
ON CONFLICT (name) DO NOTHING;

-- 문구 / Stationery
INSERT INTO objects (name, name_en, category, category_en) VALUES
('연필', 'Pencil', '문구', 'Stationery'), ('지우개', 'Eraser', '문구', 'Stationery'), ('자', 'Ruler', '문구', 'Stationery'), ('컴퍼스', 'Compass', '문구', 'Stationery'),
('스테이플러', 'Stapler', '문구', 'Stationery'), ('테이프', 'Tape', '문구', 'Stationery'), ('클립', 'Paper Clip', '문구', 'Stationery'), ('포스트잇', 'Post-it', '문구', 'Stationery'),
('화이트보드', 'Whiteboard', '문구', 'Stationery'), ('프로젝터', 'Projector', '문구', 'Stationery'), ('프린터', 'Printer', '문구', 'Stationery'), ('복사기', 'Copy Machine', '문구', 'Stationery')
ON CONFLICT (name) DO NOTHING;

-- 장난감 / Toys
INSERT INTO objects (name, name_en, category, category_en) VALUES
('레고', 'Lego', '장난감', 'Toy'), ('인형', 'Doll', '장난감', 'Toy'), ('요요', 'Yo-Yo', '장난감', 'Toy'), ('팽이', 'Spinning Top', '장난감', 'Toy'),
('퍼즐', 'Puzzle', '장난감', 'Toy'), ('루빅스큐브', 'Rubiks Cube', '장난감', 'Toy'), ('슬라임', 'Slime', '장난감', 'Toy'), ('비눗방울', 'Soap Bubbles', '장난감', 'Toy'),
('물총', 'Water Gun', '장난감', 'Toy'), ('너프건', 'Nerf Gun', '장난감', 'Toy'), ('장난감드론', 'Toy Drone', '장난감', 'Toy'), ('RC카', 'RC Car', '장난감', 'Toy'),
('보드게임', 'Board Game', '장난감', 'Toy'), ('트럼프카드', 'Playing Cards', '장난감', 'Toy'), ('주사위', 'Dice', '장난감', 'Toy'), ('다트판', 'Dartboard', '장난감', 'Toy')
ON CONFLICT (name) DO NOTHING;

-- 의료 / Medical
INSERT INTO objects (name, name_en, category, category_en) VALUES
('주사기', 'Syringe', '의료', 'Medical'), ('청진기', 'Stethoscope', '의료', 'Medical'), ('붕대', 'Bandage', '의료', 'Medical'), ('목발', 'Crutch', '의료', 'Medical'),
('휠체어', 'Wheelchair', '의료', 'Medical'), ('깁스', 'Cast', '의료', 'Medical'), ('체온계', 'Thermometer', '의료', 'Medical'), ('혈압계', 'Blood Pressure Monitor', '의료', 'Medical'),
('현미경', 'Microscope', '의료', 'Medical'), ('엑스레이', 'X-Ray Machine', '의료', 'Medical'), ('MRI', 'MRI Machine', '의료', 'Medical'), ('제세동기', 'Defibrillator', '의료', 'Medical')
ON CONFLICT (name) DO NOTHING;

-- 주방 / Kitchen
INSERT INTO objects (name, name_en, category, category_en) VALUES
('프라이팬', 'Frying Pan', '주방', 'Kitchen'), ('냄비', 'Pot', '주방', 'Kitchen'), ('국자', 'Ladle', '주방', 'Kitchen'), ('뒤집개', 'Spatula', '주방', 'Kitchen'),
('도마', 'Cutting Board', '주방', 'Kitchen'), ('믹서', 'Mixer', '주방', 'Kitchen'), ('오븐', 'Oven', '주방', 'Kitchen'), ('에어프라이어', 'Air Fryer', '주방', 'Kitchen'),
('커피머신', 'Coffee Machine', '주방', 'Kitchen'), ('와플메이커', 'Waffle Maker', '주방', 'Kitchen'), ('식기세척기', 'Dishwasher', '주방', 'Kitchen'), ('정수기', 'Water Purifier', '주방', 'Kitchen')
ON CONFLICT (name) DO NOTHING;

-- 캠핑 / Camping
INSERT INTO objects (name, name_en, category, category_en) VALUES
('캠핑의자', 'Camp Chair', '캠핑', 'Camping'), ('랜턴', 'Lantern', '캠핑', 'Camping'), ('침낭', 'Sleeping Bag', '캠핑', 'Camping'), ('해먹', 'Hammock', '캠핑', 'Camping'),
('쿨러', 'Cooler', '캠핑', 'Camping'), ('버너', 'Burner', '캠핑', 'Camping'), ('코펠', 'Mess Kit', '캠핑', 'Camping'), ('타프', 'Tarp', '캠핑', 'Camping'),
('등산스틱', 'Hiking Pole', '캠핑', 'Camping'), ('나침반', 'Compass', '캠핑', 'Camping'), ('맥가이버칼', 'Swiss Army Knife', '캠핑', 'Camping'), ('라이터', 'Lighter', '캠핑', 'Camping')
ON CONFLICT (name) DO NOTHING;

-- 전자기기 / Electronics
INSERT INTO objects (name, name_en, category, category_en) VALUES
('노트북', 'Laptop', '전자기기', 'Electronics'), ('태블릿', 'Tablet', '전자기기', 'Electronics'), ('스마트워치', 'Smartwatch', '전자기기', 'Electronics'), ('이어폰', 'Earbuds', '전자기기', 'Electronics'),
('스피커', 'Speaker', '전자기기', 'Electronics'), ('카메라', 'Camera', '전자기기', 'Electronics'), ('빔프로젝터', 'Beam Projector', '전자기기', 'Electronics'), ('게임기', 'Game Console', '전자기기', 'Electronics'),
('VR헤드셋', 'VR Headset', '전자기기', 'Electronics'), ('킨들', 'Kindle', '전자기기', 'Electronics'), ('GPS', 'GPS', '전자기기', 'Electronics'), ('웹캠', 'Webcam', '전자기기', 'Electronics')
ON CONFLICT (name) DO NOTHING;

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

-- =====================
-- Additional: Creatures
-- =====================

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
-- Encounter scripts table
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
