#!/bin/bash

# n8n 워크플로우 내보내기 스크립트
# 사용법: ./scripts/export-workflow.sh
#
# 현재 n8n에 있는 모든 워크플로우를 /workflows/ 폴더로 내보내기

set -e

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="$SCRIPT_DIR/.."
ENV_FILE="$PROJECT_DIR/.env"
WORKFLOWS_DIR="$PROJECT_DIR/workflows"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== n8n 워크플로우 내보내기 ===${NC}"
echo ""

# .env 파일에서 N8N_API_KEY 읽기
if [ -f "$ENV_FILE" ]; then
  export $(grep -E '^N8N_API_KEY=' "$ENV_FILE" | xargs)
fi

if [ -z "$N8N_API_KEY" ]; then
  echo -e "${RED}오류: N8N_API_KEY가 설정되지 않았습니다.${NC}"
  exit 1
fi

N8N_URL="http://localhost:5678"

# n8n 연결 확인
echo "n8n 연결 확인 중..."
if ! curl -s "$N8N_URL/healthz" > /dev/null 2>&1; then
  echo -e "${RED}오류: n8n에 연결할 수 없습니다.${NC}"
  exit 1
fi
echo -e "${GREEN}n8n 연결 성공${NC}"
echo ""

# workflows 폴더 생성
mkdir -p "$WORKFLOWS_DIR"

# 기존 JSON 파일 삭제
echo -e "${YELLOW}기존 JSON 파일 정리 중...${NC}"
rm -f "$WORKFLOWS_DIR"/*.json
echo ""

# 워크플로우 목록 가져오기
echo -e "${YELLOW}워크플로우 내보내기 중...${NC}"
WORKFLOWS=$(curl -s "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY")

WORKFLOW_IDS=$(echo "$WORKFLOWS" | jq -r '.data[].id' 2>/dev/null)

if [ -z "$WORKFLOW_IDS" ]; then
  echo "내보낼 워크플로우 없음"
  exit 0
fi

# 각 워크플로우 상세 정보 가져와서 저장
for ID in $WORKFLOW_IDS; do
  WORKFLOW=$(curl -s "$N8N_URL/api/v1/workflows/$ID" \
    -H "X-N8N-API-KEY: $N8N_API_KEY")

  NAME=$(echo "$WORKFLOW" | jq -r '.name' 2>/dev/null)
  FILENAME="$WORKFLOWS_DIR/$ID.json"

  echo "$WORKFLOW" | jq '.' > "$FILENAME"
  echo -e "  ${GREEN}✓${NC} $NAME → $ID.json"
done

echo ""
echo -e "${GREEN}=== 내보내기 완료 ===${NC}"
echo ""
echo "저장 위치: $WORKFLOWS_DIR"
ls -la "$WORKFLOWS_DIR"/*.json 2>/dev/null | awk '{print "  " $NF}'
