FROM node:20-slim

# Chromium 의존성 설치 (Remotion 렌더링에 필요)
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-noto-cjk \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# package.json 먼저 복사하여 캐시 활용
COPY package*.json ./
RUN npm install

# 소스 복사
COPY . .

# 포트 노출
EXPOSE 3001

# 서버 실행
CMD ["npm", "run", "server"]
