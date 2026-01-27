#!/bin/bash

# Git pre-commit hook
# commit 전에 credentials와 workflows를 자동으로 내보내기
# 설치: ln -sf ../../scripts/pre-commit.sh .git/hooks/pre-commit

# 심링크를 따라가서 실제 스크립트 위치를 찾음
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || realpath "$0" 2>/dev/null || echo "$0")")" && pwd)

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[pre-commit] n8n 데이터 동기화 중...${NC}"

# n8n 컨테이너가 실행 중인지 확인
if ! docker ps | grep -q "n8n"; then
  echo -e "${RED}[pre-commit] 오류: n8n 컨테이너가 실행 중이 아닙니다.${NC}"
  echo -e "${RED}docker compose up -d 로 컨테이너를 실행한 후 다시 시도하세요.${NC}"
  exit 1
fi

# credentials 내보내기
echo "[pre-commit] credentials 내보내기..."
if ! "$SCRIPT_DIR/export-credentials.sh" > /dev/null 2>&1; then
  echo -e "${RED}[pre-commit] 오류: credentials 내보내기 실패${NC}"
  exit 1
fi

# workflows 내보내기
echo "[pre-commit] workflows 내보내기..."
if ! "$SCRIPT_DIR/export-workflow.sh" > /dev/null 2>&1; then
  echo -e "${RED}[pre-commit] 오류: workflows 내보내기 실패${NC}"
  exit 1
fi

# 변경된 파일 staging
git add credentials/credentials.json 2>/dev/null
git add workflows/*.json 2>/dev/null

echo -e "${GREEN}[pre-commit] 동기화 완료${NC}"
exit 0
