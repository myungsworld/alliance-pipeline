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
