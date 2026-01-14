# Dockerfile - Alliance Pipeline
# Python 3.11 + Chrome 기반 이미지

FROM python:3.11-slim

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    # Chrome 의존성
    libnss3 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libgtk-3-0 \
    libgbm1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxrandr2 \
    libxshmfence1 \
    libdrm2 \
    libpango-1.0-0 \
    libcairo2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    # 정리
    && rm -rf /var/lib/apt/lists/*

# Chrome/Chromium 설치 (아키텍처 자동 감지)
RUN apt-get update && \
    if [ "$(dpkg --print-architecture)" = "amd64" ]; then \
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
        apt-get update && \
        apt-get install -y google-chrome-stable; \
    else \
        apt-get install -y chromium chromium-driver; \
    fi && \
    rm -rf /var/lib/apt/lists/*

# Chrome 바이너리 환경변수 설정
ENV CHROME_BIN=/usr/bin/chromium

# 작업 디렉토리
WORKDIR /app

# 의존성 파일 복사
COPY pyproject.toml .

# Python 의존성 설치
RUN pip install --no-cache-dir pip --upgrade \
    && pip install --no-cache-dir pydantic pyyaml httpx python-dotenv beautifulsoup4 \
    && pip install --no-cache-dir selenium undetected-chromedriver \
    && pip install --no-cache-dir fastapi uvicorn || true

# 소스 코드 복사
COPY . .

# 데이터 디렉토리 생성
RUN mkdir -p data/cache data/logs data/db data/sessions

# 환경변수
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# 기본 명령어
CMD ["python", "scripts/run.py", "server"]
