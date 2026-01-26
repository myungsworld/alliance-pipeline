#!/bin/bash

# n8n 워크플로우 삭제 스크립트
# 사용법: ./scripts/delete-workflow.sh <워크플로우ID>

if [ -z "$1" ]; then
  echo "사용법: $0 <워크플로우ID>"
  echo "예시: $0 vJuofocpk-8erRDTSVyfI"
  exit 1
fi

WORKFLOW_ID=$1
SCRIPT_DIR=$(dirname "$0")
ENV_FILE="$SCRIPT_DIR/../.env"

# .env 파일에서 N8N_API_KEY 읽기
if [ -f "$ENV_FILE" ]; then
  export $(grep -E '^N8N_API_KEY=' "$ENV_FILE" | xargs)
fi

if [ -z "$N8N_API_KEY" ]; then
  echo "오류: N8N_API_KEY가 설정되지 않았습니다."
  echo ".env 파일에 N8N_API_KEY를 추가하거나 환경변수로 설정하세요."
  exit 1
fi

echo "워크플로우 삭제 중: $WORKFLOW_ID"

curl -X DELETE "http://localhost:5678/api/v1/workflows/$WORKFLOW_ID" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -s | jq -r '.name // .message' 2>/dev/null || echo "삭제 완료 (또는 이미 삭제됨)"

echo ""
echo "완료!"
