# 使用官方 Python 3.11 映像檔為基底
FROM python:3.11-slim

# 設定環境變數避免產生 .pyc 與不緩衝 stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 設定工作目錄
WORKDIR /code

# 安裝系統相依套件 (編譯 psycopg2 等套件可能需要)
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# 設定啟動指令，這裡預設執行 FastAPI 應用程式
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
