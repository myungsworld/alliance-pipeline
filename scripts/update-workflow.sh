#!/bin/bash

# n8n 워크플로우 동기화 스크립트
# 사용법: ./scripts/update-workflow.sh
#
# 1. 현재 n8n에 있는 모든 워크플로우 삭제
# 2. /workflows/ 폴더의 JSON 파일들을 모두 import

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="$SCRIPT_DIR/.."
ENV_FILE="$PROJECT_DIR/.env"
WORKFLOWS_DIR="$PROJECT_DIR/workflows"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== n8n 워크플로우 동기화 ===${NC}"
echo ""

# .env 파일에서 N8N_API_KEY 읽기
if [ -f "$ENV_FILE" ]; then
  N8N_API_KEY=$(grep -E '^N8N_API_KEY=' "$ENV_FILE" | cut -d '=' -f2)
fi

if [ -z "$N8N_API_KEY" ]; then
  echo -e "${RED}오류: N8N_API_KEY가 설정되지 않았습니다.${NC}"
  echo ".env 파일에 N8N_API_KEY를 추가하거나 환경변수로 설정하세요."
  exit 1
fi

N8N_URL="http://localhost:5678"

# n8n 연결 확인
echo "n8n 연결 확인 중..."
if ! curl -s "$N8N_URL/healthz" > /dev/null 2>&1; then
  echo -e "${RED}오류: n8n에 연결할 수 없습니다. Docker가 실행 중인지 확인하세요.${NC}"
  exit 1
fi
echo -e "${GREEN}n8n 연결 성공${NC}"
echo ""

# 1단계: 현재 워크플로우 목록 가져오기
echo -e "${YELLOW}[1/3] 현재 워크플로우 목록 조회 중...${NC}"
WORKFLOWS=$(curl -s "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY")

WORKFLOW_IDS=$(echo "$WORKFLOWS" | jq -r '.data[].id' 2>/dev/null)

if [ -z "$WORKFLOW_IDS" ]; then
  echo "기존 워크플로우 없음"
else
  echo "발견된 워크플로우:"
  echo "$WORKFLOWS" | jq -r '.data[] | "  - \(.id): \(.name)"' 2>/dev/null
fi
echo ""

# 2단계: 모든 워크플로우 삭제
echo -e "${YELLOW}[2/3] 기존 워크플로우 삭제 중...${NC}"
if [ -n "$WORKFLOW_IDS" ]; then
  for ID in $WORKFLOW_IDS; do
    NAME=$(echo "$WORKFLOWS" | jq -r ".data[] | select(.id==\"$ID\") | .name" 2>/dev/null)
    echo -n "  삭제: $NAME ($ID)... "
    curl -s -X DELETE "$N8N_URL/api/v1/workflows/$ID" \
      -H "X-N8N-API-KEY: $N8N_API_KEY" > /dev/null
    echo -e "${GREEN}완료${NC}"
  done
else
  echo "  삭제할 워크플로우 없음"
fi
echo ""

# 3단계: workflows/ 폴더에서 JSON 파일 import
echo -e "${YELLOW}[3/3] 워크플로우 import 중...${NC}"

if [ ! -d "$WORKFLOWS_DIR" ]; then
  echo -e "${RED}오류: workflows/ 폴더를 찾을 수 없습니다.${NC}"
  exit 1
fi

JSON_FILES=$(find "$WORKFLOWS_DIR" -name "*.json" -type f 2>/dev/null)

if [ -z "$JSON_FILES" ]; then
  echo "  import할 JSON 파일 없음"
else
  for JSON_FILE in $JSON_FILES; do
    FILENAME=$(basename "$JSON_FILE")
    WORKFLOW_NAME=$(jq -r '.name' "$JSON_FILE" 2>/dev/null)

    if [ -z "$WORKFLOW_NAME" ] || [ "$WORKFLOW_NAME" = "null" ]; then
      WORKFLOW_NAME="$FILENAME"
    fi

    echo -n "  import: $WORKFLOW_NAME... "

    # 워크플로우 생성 (API가 허용하는 필드만 추출)
    IMPORT_DATA=$(jq '{name, nodes, connections, settings, staticData}' "$JSON_FILE" 2>/dev/null)

    RESULT=$(curl -s -X POST "$N8N_URL/api/v1/workflows" \
      -H "X-N8N-API-KEY: $N8N_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$IMPORT_DATA")

    NEW_ID=$(echo "$RESULT" | jq -r '.id' 2>/dev/null)

    if [ -n "$NEW_ID" ] && [ "$NEW_ID" != "null" ]; then
      echo -e "${GREEN}완료${NC} (ID: $NEW_ID)"

      # 워크플로우 활성화
      curl -s -X PATCH "$N8N_URL/api/v1/workflows/$NEW_ID" \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"active": true}' > /dev/null 2>&1
    else
      ERROR=$(echo "$RESULT" | jq -r '.message' 2>/dev/null)
      echo -e "${RED}실패${NC} ($ERROR)"
    fi
  done
fi

echo ""
echo -e "${GREEN}=== 동기화 완료 ===${NC}"
echo ""

# 최종 워크플로우 목록 출력
echo "현재 워크플로우 목록:"
curl -s "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq -r '.data[] | "  - \(.name) (active: \(.active))"' 2>/dev/null

echo ""
