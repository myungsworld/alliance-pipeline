# Claude 컨텍스트

새 세션 시작시 이 파일을 먼저 읽어서 프로젝트 상태를 파악하세요.

## 프로젝트 개요

**목적**: 쿠팡 파트너스 제휴 마케팅 자동화
**언어**: Python 3.11
**실행환경**: Docker

## 프로젝트 구조

```
src/
├── core/           # 공통 모듈 (설정, 이벤트, 저장소, 큐, 스케줄러)
├── browser/        # 스텔스 브라우저 (undetected-chromedriver)
│   ├── engine/     # 드라이버, 세션, 풀
│   ├── stealth/    # 탐지 우회 (webdriver 숨김, fingerprint)
│   ├── human/      # 사람 행동 (마우스, 키보드, 스크롤)
│   └── proxy/      # 프록시 관리
├── actions/        # 브라우저 액션 (네이버, 아마존)
├── scrapers/       # 크롤러 (쿠팡)
├── publishers/     # 발행 채널 (티스토리, 텔레그램)
├── pipelines/      # 파이프라인 빌더
└── transport/      # CLI, HTTP API
```

## 핵심 설계 패턴

**어댑터 패턴**: 모든 컴포넌트는 인터페이스 기반으로 교체 가능
```python
StorageRegistry.get("file")    # 또는 "sqlite", "mysql"
PublisherRegistry.get("tistory")  # 또는 "telegram"
```

## 현재 상태

- **버전**: 0.1.0
- **마지막 작업**: 초기 구조 완성
- **다음 작업**: Docker 테스트

## 체크리스트

새 세션에서 작업 시작 전:
1. `README.md` - 현재 상태, TODO 확인
2. `docker-compose.yaml` - Docker 설정 확인
3. `config/secrets.yaml.example` - 필요한 API 키 확인

## 자주 쓰는 명령어 (Makefile)

```bash
make help       # 전체 명령어 보기
make build      # Docker 빌드
make up         # 컨테이너 시작
make down       # 컨테이너 중지
make logs       # 로그 보기
make shell      # 컨테이너 쉘 접속

make scrape     # 쿠팡 할인 크롤링 테스트
make pipeline   # 파이프라인 실행
make list       # 플러그인 목록

make init       # 초기 설정 (secrets.yaml 생성)
```

## 파일 변경시 업데이트 필요

- 새 모듈 추가 → 이 파일의 프로젝트 구조 업데이트
- TODO 완료 → README.md 체크리스트 업데이트
- Docker 설정 변경 → docker-compose.yaml 수정
- 의존성 추가 → pyproject.toml 수정
