from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import attendance, chat, auth, users, leave

# 啟動時自動建立所有的資料庫表格 (正式環境通常由 Alembic 代勞，這裡為了方便測試)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance System", version="1.0.0")

# 掛載靜態檔案目錄（讓 /static/main.js 等外部 JS/CSS 可被正常存取）
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 設定模板目錄
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# 註冊 API 路由
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(leave.router, prefix="/api/leave", tags=["Leave"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """回傳前端首頁"""
    return templates.TemplateResponse(request=request, name="index.html")
