#!/bin/bash

# n8n 크레덴셜 가져오기 스크립트
# 사용법: ./scripts/import-credentials.sh

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="$SCRIPT_DIR/.."
CREDENTIALS_FILE="$PROJECT_DIR/credentials/credentials.json"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== n8n 크레덴셜 가져오기 ===${NC}"
echo ""

# credentials.json 파일 확인
if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo -e "${RED}오류: credentials.json 파일을 찾을 수 없습니다.${NC}"
  echo "먼저 ./scripts/export-credentials.sh 를 실행하거나"
  echo "다른 PC에서 credentials.json을 복사하세요."
  exit 1
fi

# Docker 컨테이너 확인
if ! docker ps | grep -q "n8n"; then
  echo -e "${RED}오류: n8n 컨테이너가 실행 중이 아닙니다.${NC}"
  exit 1
fi

# 가져올 크레덴셜 목록 표시
echo "가져올 크레덴셜:"
jq -r '.[] | "  - \(.name) (\(.type))"' "$CREDENTIALS_FILE" 2>/dev/null
echo ""

# 로컬에서 컨테이너로 복사
echo "크레덴셜 복사 중..."
docker cp "$CREDENTIALS_FILE" n8n:/home/node/credentials.json

if [ $? -ne 0 ]; then
  echo -e "${RED}오류: 파일 복사 실패${NC}"
  exit 1
fi

# 크레덴셜 가져오기 (컨테이너 내부에서 실행)
echo "크레덴셜 가져오기 중..."
docker exec -u node n8n n8n import:credentials --input=/home/node/credentials.json

if [ $? -eq 0 ]; then
  echo ""
  echo -e "${GREEN}=== 가져오기 완료 ===${NC}"
else
  echo -e "${RED}오류: 크레덴셜 가져오기 실패${NC}"
  echo ""
  echo "이미 동일한 이름의 크레덴셜이 존재할 수 있습니다."
  echo "n8n UI에서 기존 크레덴셜을 삭제 후 다시 시도하세요."
fi

# 컨테이너 내부 파일 정리
docker exec -u node n8n rm -f /home/node/credentials.json 2>/dev/null

echo ""
