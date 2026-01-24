-- 물건 테이블
CREATE TABLE objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 생명체 테이블
CREATE TABLE creatures (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 사용된 조합 기록 (중복 방지)
CREATE TABLE combinations_used (
    id SERIAL PRIMARY KEY,
    object_id INT REFERENCES objects(id),
    creature_id INT REFERENCES creatures(id),
    content_type VARCHAR(50),
    used_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(object_id, creature_id, content_type)
);

-- 인덱스 생성
CREATE INDEX idx_objects_category ON objects(category);
CREATE INDEX idx_creatures_category ON creatures(category);

-- =====================
-- 초기 데이터: 물건
-- =====================

-- 도구
INSERT INTO objects (name, category) VALUES
('망치', '도구'), ('칼', '도구'), ('우산', '도구'), ('가위', '도구'),
('열쇠', '도구'), ('손전등', '도구'), ('망원경', '도구'), ('돋보기', '도구'),
('낚싯대', '도구'), ('삽', '도구'), ('톱', '도구'), ('펜치', '도구');

-- 가전
INSERT INTO objects (name, category) VALUES
('에어컨', '가전'), ('냉장고', '가전'), ('TV', '가전'), ('세탁기', '가전'),
('전자레인지', '가전'), ('청소기', '가전'), ('선풍기', '가전'), ('토스터', '가전'),
('믹서기', '가전'), ('다리미', '가전'), ('헤어드라이어', '가전'), ('전기밥솥', '가전');

-- 탈것
INSERT INTO objects (name, category) VALUES
('자동차', '탈것'), ('비행기', '탈것'), ('로켓', '탈것'), ('자전거', '탈것'),
('오토바이', '탈것'), ('헬리콥터', '탈것'), ('잠수함', '탈것'), ('요트', '탈것'),
('스케이트보드', '탈것'), ('썰매', '탈것'), ('열기구', '탈것'), ('제트스키', '탈것');

-- 악기
INSERT INTO objects (name, category) VALUES
('피아노', '악기'), ('기타', '악기'), ('드럼', '악기'), ('바이올린', '악기'),
('트럼펫', '악기'), ('플루트', '악기'), ('하프', '악기'), ('색소폰', '악기'),
('아코디언', '악기'), ('탬버린', '악기'), ('실로폰', '악기'), ('우쿨렐레', '악기');

-- 무기
INSERT INTO objects (name, category) VALUES
('검', '무기'), ('방패', '무기'), ('활', '무기'), ('창', '무기'),
('도끼', '무기'), ('석궁', '무기'), ('삼지창', '무기'), ('철퇴', '무기'),
('부메랑', '무기'), ('표창', '무기'), ('쌍절곤', '무기'), ('채찍', '무기');

-- 일상용품
INSERT INTO objects (name, category) VALUES
('물컵', '일상용품'), ('휴대폰', '일상용품'), ('책', '일상용품'), ('신발', '일상용품'),
('안경', '일상용품'), ('시계', '일상용품'), ('지갑', '일상용품'), ('가방', '일상용품'),
('모자', '일상용품'), ('장갑', '일상용품'), ('목도리', '일상용품'), ('양말', '일상용품');

-- 가구
INSERT INTO objects (name, category) VALUES
('의자', '가구'), ('책상', '가구'), ('침대', '가구'), ('소파', '가구'),
('옷장', '가구'), ('책장', '가구'), ('식탁', '가구'), ('서랍장', '가구'),
('거울', '가구'), ('화장대', '가구'), ('신발장', '가구'), ('행거', '가구');

-- 스포츠용품
INSERT INTO objects (name, category) VALUES
('축구공', '스포츠'), ('야구방망이', '스포츠'), ('테니스라켓', '스포츠'), ('골프채', '스포츠'),
('농구공', '스포츠'), ('배드민턴라켓', '스포츠'), ('스키', '스포츠'), ('스노보드', '스포츠'),
('권투글러브', '스포츠'), ('볼링공', '스포츠'), ('다트', '스포츠'), ('탁구채', '스포츠');

-- =====================
-- 초기 데이터: 생명체
-- =====================

-- 포유류
INSERT INTO creatures (name, category) VALUES
('고양이', '포유류'), ('강아지', '포유류'), ('사자', '포유류'), ('호랑이', '포유류'),
('코끼리', '포유류'), ('기린', '포유류'), ('곰', '포유류'), ('늑대', '포유류'),
('여우', '포유류'), ('토끼', '포유류'), ('다람쥐', '포유류'), ('햄스터', '포유류'),
('판다', '포유류'), ('코알라', '포유류'), ('캥거루', '포유류'), ('하마', '포유류');

-- 조류
INSERT INTO creatures (name, category) VALUES
('펭귄', '조류'), ('닭', '조류'), ('독수리', '조류'), ('앵무새', '조류'),
('부엉이', '조류'), ('플라밍고', '조류'), ('공작', '조류'), ('까마귀', '조류'),
('비둘기', '조류'), ('참새', '조류'), ('오리', '조류'), ('거위', '조류');

-- 수중생물
INSERT INTO creatures (name, category) VALUES
('상어', '수중생물'), ('고래', '수중생물'), ('돌고래', '수중생물'), ('문어', '수중생물'),
('오징어', '수중생물'), ('해파리', '수중생물'), ('거북이', '수중생물'), ('게', '수중생물'),
('새우', '수중생물'), ('불가사리', '수중생물'), ('조개', '수중생물'), ('해마', '수중생물');

-- 파충류/양서류
INSERT INTO creatures (name, category) VALUES
('공룡', '파충류'), ('악어', '파충류'), ('뱀', '파충류'), ('도마뱀', '파충류'),
('카멜레온', '파충류'), ('이구아나', '파충류'), ('개구리', '양서류'), ('도롱뇽', '양서류');

-- 곤충
INSERT INTO creatures (name, category) VALUES
('꿀벌', '곤충'), ('나비', '곤충'), ('개미', '곤충'), ('무당벌레', '곤충'),
('잠자리', '곤충'), ('반딧불이', '곤충'), ('귀뚜라미', '곤충'), ('사마귀', '곤충');

-- 상상의 동물
INSERT INTO creatures (name, category) VALUES
('드래곤', '상상'), ('유니콘', '상상'), ('피닉스', '상상'), ('그리핀', '상상'),
('페가수스', '상상'), ('켄타우로스', '상상'), ('미노타우로스', '상상'), ('키메라', '상상'),
('크라켄', '상상'), ('고블린', '상상'), ('트롤', '상상'), ('오크', '상상'),
('엘프', '상상'), ('요정', '상상'), ('인어', '상상'), ('늑대인간', '상상');

-- 인간형/기타
INSERT INTO creatures (name, category) VALUES
('로봇', '기타'), ('외계인', '기타'), ('좀비', '기타'), ('해골', '기타'),
('유령', '기타'), ('닌자', '기타'), ('해적', '기타'), ('기사', '기타'),
('마법사', '기타'), ('슈퍼히어로', '기타'), ('거인', '기타'), ('난쟁이', '기타');

-- 랜덤 조합 뷰 (사용 안 된 조합만)
CREATE VIEW random_unused_combination AS
SELECT
    o.id as object_id,
    o.name as object_name,
    o.category as object_category,
    c.id as creature_id,
    c.name as creature_name,
    c.category as creature_category
FROM objects o
CROSS JOIN creatures c
WHERE NOT EXISTS (
    SELECT 1 FROM combinations_used cu
    WHERE cu.object_id = o.id AND cu.creature_id = c.id
)
ORDER BY RANDOM()
LIMIT 1;
