#!/bin/bash

# n8n 워크플로우 내보내기 스크립트
# 사용법: ./scripts/export-workflow.sh
#
# 워크플로우를 이름 기반으로 저장 (기존 폴더 구조 유지)
# - 이미 존재하는 워크플로우: 기존 위치에서 업데이트
# - 새 워크플로우: workflows/ 루트에 저장

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

# 워크플로우 이름을 파일명으로 변환 (공백 → -, 특수문자 제거)
sanitize_name() {
  echo "$1" | tr ' ' '-' | tr -cd '[:alnum:]-_'
}

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

# 워크플로우 목록 가져오기
echo -e "${YELLOW}워크플로우 내보내기 중...${NC}"
WORKFLOWS=$(curl -s "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY")

WORKFLOW_IDS=$(echo "$WORKFLOWS" | jq -r '.data[].id' 2>/dev/null)

if [ -z "$WORKFLOW_IDS" ]; then
  echo "내보낼 워크플로우 없음"
  exit 0
fi

# n8n에 있는 워크플로우 이름 목록 수집 (나중에 삭제된 것 찾기 위함)
EXPORTED_NAMES=""

# 각 워크플로우 상세 정보 가져와서 저장
for ID in $WORKFLOW_IDS; do
  WORKFLOW=$(curl -s "$N8N_URL/api/v1/workflows/$ID" \
    -H "X-N8N-API-KEY: $N8N_API_KEY")

  NAME=$(echo "$WORKFLOW" | jq -r '.name' 2>/dev/null)
  SAFE_NAME=$(sanitize_name "$NAME")

  EXPORTED_NAMES="$EXPORTED_NAMES $SAFE_NAME"

  # 기존 파일 찾기 (하위 폴더 포함)
  EXISTING_FILE=$(find "$WORKFLOWS_DIR" -name "${SAFE_NAME}.json" -type f 2>/dev/null | head -1)

  if [ -n "$EXISTING_FILE" ]; then
    # 기존 위치에 업데이트
    FILENAME="$EXISTING_FILE"
    RELATIVE_PATH="${EXISTING_FILE#$WORKFLOWS_DIR/}"
  else
    # 새 워크플로우는 폴더 생성 후 저장
    mkdir -p "$WORKFLOWS_DIR/${SAFE_NAME}"
    FILENAME="$WORKFLOWS_DIR/${SAFE_NAME}/${SAFE_NAME}.json"
    RELATIVE_PATH="${SAFE_NAME}/${SAFE_NAME}.json"
  fi

  echo "$WORKFLOW" | jq '.' > "$FILENAME"
  echo -e "  ${GREEN}✓${NC} $NAME → $RELATIVE_PATH"
done

# n8n에서 삭제된 워크플로우 파일 정리
echo ""
echo -e "${YELLOW}삭제된 워크플로우 정리 중...${NC}"
DELETED_COUNT=0
while IFS= read -r file; do
  if [ -n "$file" ]; then
    BASENAME=$(basename "$file" .json)
    if ! echo "$EXPORTED_NAMES" | grep -qw "$BASENAME"; then
      rm -f "$file"
      echo -e "  ${RED}✗${NC} 삭제: $file"
      DELETED_COUNT=$((DELETED_COUNT + 1))
    fi
  fi
done < <(find "$WORKFLOWS_DIR" -name "*.json" -type f 2>/dev/null)

if [ "$DELETED_COUNT" -eq 0 ]; then
  echo "  삭제된 워크플로우 없음"
fi

echo ""
echo -e "${GREEN}=== 내보내기 완료 ===${NC}"
echo ""
echo "저장 위치:"
find "$WORKFLOWS_DIR" -name "*.json" -type f | sort | while read f; do
  echo "  ${f#$WORKFLOWS_DIR/}"
done
