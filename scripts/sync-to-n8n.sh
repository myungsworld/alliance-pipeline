#!/bin/bash

# n8n 동기화 스크립트 (credentials + workflows)
# 사용법: ./scripts/sync-to-n8n.sh
#
# 1. credentials.json → n8n import (동일 ID는 덮어쓰기)
# 2. 기존 workflows 전부 삭제
# 3. workflows/*.json import + 활성화 (단일 워크플로우)

set -e

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="$SCRIPT_DIR/.."
ENV_FILE="$PROJECT_DIR/.env"
CREDENTIALS_FILE="$PROJECT_DIR/credentials/credentials.json"
WORKFLOWS_DIR="$PROJECT_DIR/workflows"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== n8n 동기화 시작 ===${NC}"
echo ""

# .env 파일에서 N8N_API_KEY 읽기
if [ -f "$ENV_FILE" ]; then
  N8N_API_KEY=$(grep -E '^N8N_API_KEY=' "$ENV_FILE" | cut -d '=' -f2)
fi

if [ -z "$N8N_API_KEY" ]; then
  echo -e "${RED}오류: N8N_API_KEY가 설정되지 않았습니다.${NC}"
  exit 1
fi

N8N_URL="http://localhost:5678"

# Docker 컨테이너 확인
if ! docker ps | grep -q "n8n"; then
  echo -e "${RED}오류: n8n 컨테이너가 실행 중이 아닙니다.${NC}"
  exit 1
fi

# n8n 연결 확인
echo "n8n 연결 확인 중..."
if ! curl -s "$N8N_URL/healthz" > /dev/null 2>&1; then
  echo -e "${RED}오류: n8n에 연결할 수 없습니다.${NC}"
  exit 1
fi
echo -e "${GREEN}n8n 연결 성공${NC}"
echo ""

# =============================================
# 1. Credentials import (CLI - 동일 ID 덮어쓰기)
# =============================================
echo -e "${YELLOW}[1/3] credentials import 중...${NC}"

if [ ! -f "$CREDENTIALS_FILE" ]; then
  echo -e "${RED}오류: credentials.json 파일을 찾을 수 없습니다.${NC}"
  exit 1
fi

jq -r '.[] | "  - \(.name) (\(.type))"' "$CREDENTIALS_FILE" 2>/dev/null

docker cp "$CREDENTIALS_FILE" n8n:/home/node/credentials.json
docker exec -i -u node n8n n8n import:credentials --input=/home/node/credentials.json 2>&1 || {
  echo -e "${RED}credentials import 실패 - 수동 확인 필요${NC}"
  echo "수동 실행: docker exec -it -u node n8n n8n import:credentials --input=/home/node/credentials.json"
}
docker exec -u node n8n rm -f /home/node/credentials.json 2>/dev/null

echo -e "${GREEN}credentials import 완료${NC}"
echo ""

# =============================================
# 2. Workflows 삭제 (REST API)
# =============================================
echo -e "${YELLOW}[2/3] 기존 workflows 삭제 중...${NC}"

WORKFLOWS=$(curl -s "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY")
WORKFLOW_IDS=$(echo "$WORKFLOWS" | jq -r '.data[].id' 2>/dev/null)

if [ -n "$WORKFLOW_IDS" ]; then
  for ID in $WORKFLOW_IDS; do
    NAME=$(echo "$WORKFLOWS" | jq -r ".data[] | select(.id==\"$ID\") | .name" 2>/dev/null)
    echo -n "  삭제: $NAME ($ID)... "
    curl -s -X DELETE "$N8N_URL/api/v1/workflows/$ID" \
      -H "X-N8N-API-KEY: $N8N_API_KEY" > /dev/null
    echo -e "${GREEN}완료${NC}"
  done
else
  echo "  삭제할 workflows 없음"
fi
echo ""

# =============================================
# 3. Workflows import (REST API + 활성화)
# =============================================
echo -e "${YELLOW}[3/3] workflows import 중...${NC}"

if [ ! -d "$WORKFLOWS_DIR" ]; then
  echo -e "${RED}오류: workflows/ 폴더를 찾을 수 없습니다.${NC}"
  exit 1
fi

JSON_FILES=$(find "$WORKFLOWS_DIR" -name "*.json" -type f 2>/dev/null)

IMPORTED_IDS=""

if [ -z "$JSON_FILES" ]; then
  echo "  import할 JSON 파일 없음"
else
  for JSON_FILE in $JSON_FILES; do
    WORKFLOW_NAME=$(jq -r '.name' "$JSON_FILE" 2>/dev/null)

    if [ -z "$WORKFLOW_NAME" ] || [ "$WORKFLOW_NAME" = "null" ]; then
      WORKFLOW_NAME="$(basename "$JSON_FILE")"
    fi

    echo -n "  import: $WORKFLOW_NAME... "

    IMPORT_DATA=$(jq '{name, nodes, connections, settings, staticData}' "$JSON_FILE" 2>/dev/null)

    RESULT=$(curl -s -X POST "$N8N_URL/api/v1/workflows" \
      -H "X-N8N-API-KEY: $N8N_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$IMPORT_DATA")

    NEW_ID=$(echo "$RESULT" | jq -r '.id' 2>/dev/null)

    if [ -n "$NEW_ID" ] && [ "$NEW_ID" != "null" ]; then
      IMPORTED_IDS="$IMPORTED_IDS $NEW_ID"
      echo -e "${GREEN}완료${NC} (ID: $NEW_ID)"
    else
      ERROR=$(echo "$RESULT" | jq -r '.message' 2>/dev/null)
      echo -e "${RED}실패${NC} ($ERROR)"
    fi
  done

  # 모든 워크플로우 activate (deactivate → activate로 webhook 등록 보장)
  echo ""
  echo -e "  workflows 활성화 중..."
  for WF_ID in $IMPORTED_IDS; do
    WF_NAME=$(curl -s "$N8N_URL/api/v1/workflows/$WF_ID" \
      -H "X-N8N-API-KEY: $N8N_API_KEY" | jq -r '.name' 2>/dev/null)

    echo -n "    $WF_NAME ($WF_ID): deactivate..."
    while true; do
      ACTIVE=$(curl -s -X POST "$N8N_URL/api/v1/workflows/$WF_ID/deactivate" \
        -H "X-N8N-API-KEY: $N8N_API_KEY" | jq -r '.active' 2>/dev/null)
      if [ "$ACTIVE" = "false" ]; then
        echo -n " OK → activate..."
        break
      fi
      echo -n " 재시도..."
    done

    while true; do
      ACTIVE=$(curl -s -X POST "$N8N_URL/api/v1/workflows/$WF_ID/activate" \
        -H "X-N8N-API-KEY: $N8N_API_KEY" | jq -r '.active' 2>/dev/null)
      if [ "$ACTIVE" = "true" ]; then
        echo -e " ${GREEN}OK${NC}"
        break
      fi
      echo -n " 재시도..."
    done
  done
  echo -e "  ${GREEN}활성화 완료${NC}"
fi

echo ""

echo -e "${GREEN}=== 동기화 완료 ===${NC}"
echo ""

# 최종 상태 출력
echo "현재 workflows:"
curl -s "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq -r '.data[] | "  - \(.name) (active: \(.active))"' 2>/dev/null

echo ""
