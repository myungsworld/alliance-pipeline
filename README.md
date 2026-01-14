# Alliance Pipeline

쿠팡 파트너스 제휴 마케팅 자동화 파이프라인

## 수익 구조

```
[나] → 제휴 링크 생성 → [사용자 클릭] → [구매] → [수수료 지급]
```

## 현재 상태

**버전**: 0.1.0 (초기 구조 완성)

### 구현 완료
- [x] core/ - 설정, 이벤트, 저장소, 큐, 스케줄러
- [x] browser/ - 스텔스 브라우저 (탐지 우회, 사람 행동)
- [x] actions/ - 네이버 로그인/글쓰기, 아마존 리뷰
- [x] scrapers/ - 쿠팡 상품/할인 크롤러
- [x] publishers/ - 티스토리, 텔레그램
- [x] pipelines/ - 파이프라인 빌더
- [x] transport/ - CLI, HTTP API

### TODO
- [ ] Docker 테스트
- [ ] 쿠팡 파트너스 API 연동 (제휴 링크 생성)
- [ ] 실제 발행 테스트

## 빠른 시작

```bash
make init       # secrets.yaml 생성
make build      # Docker 빌드
make up         # 컨테이너 시작
make scrape     # 크롤링 테스트
```

## 설정

`config/secrets.yaml` 필요 (secrets.yaml.example 참고)
