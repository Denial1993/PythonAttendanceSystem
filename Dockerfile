# ============================================================
# Stage 1: 建置 Vue 3 前端
# ============================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

# 先複製 package.json 利用 Docker cache
COPY frontend/package*.json ./
RUN npm ci

# 複製前端原始碼並建置
COPY frontend/ ./
RUN npm run build

# ============================================================
# Stage 2: FastAPI 後端
# ============================================================
FROM python:3.11-slim

# 設定環境變數避免產生 .pyc 與不緩衝 stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# 安裝系統相依套件
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 套件
COPY attendance_system/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# 複製後端程式碼
COPY attendance_system/ /code/

# 從 Stage 1 複製 Vue 建置產出至 FastAPI 靜態目錄
COPY --from=frontend-builder /frontend/dist /code/app/static/dist

# 設定啟動指令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
