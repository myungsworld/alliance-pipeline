#!/bin/bash

# n8n 크레덴셜 내보내기 스크립트
# 사용법: ./scripts/export-credentials.sh

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="$SCRIPT_DIR/.."
CREDENTIALS_FILE="$PROJECT_DIR/credentials/credentials.json"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== n8n 크레덴셜 내보내기 ===${NC}"
echo ""

# Docker 컨테이너 확인
if ! docker ps | grep -q "n8n"; then
  echo -e "${RED}오류: n8n 컨테이너가 실행 중이 아닙니다.${NC}"
  exit 1
fi

# credentials 폴더 생성
mkdir -p "$(dirname "$CREDENTIALS_FILE")"

# 크레덴셜 내보내기 (컨테이너 내부에서 실행)
echo "크레덴셜 내보내기 중..."
docker exec -u node n8n n8n export:credentials --all --decrypted --output=/home/node/credentials.json

if [ $? -ne 0 ]; then
  echo -e "${RED}오류: 크레덴셜 내보내기 실패${NC}"
  exit 1
fi

# 컨테이너에서 로컬로 복사
docker cp n8n:/home/node/credentials.json "$CREDENTIALS_FILE"

if [ $? -eq 0 ]; then
  echo -e "${GREEN}완료!${NC}"
  echo ""
  echo "저장 위치: $CREDENTIALS_FILE"
  echo ""

  # 크레덴셜 목록 표시
  echo "내보낸 크레덴셜:"
  jq -r '.[] | "  - \(.name) (\(.type))"' "$CREDENTIALS_FILE" 2>/dev/null

  echo ""
  echo -e "${GREEN}✅ credentials.json이 환경변수 참조로 저장되었습니다.${NC}"
  echo -e "${YELLOW}   (실제 비밀값은 .env 파일에 있음)${NC}"
else
  echo -e "${RED}오류: 파일 복사 실패${NC}"
  exit 1
fi

# 컨테이너 내부 파일 정리
docker exec -u node n8n rm -f /home/node/credentials.json 2>/dev/null

echo ""
