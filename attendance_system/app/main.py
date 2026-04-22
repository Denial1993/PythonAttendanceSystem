from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import time  # ✅ 新增這行引入 time 模組

from app.database import engine, Base
from app.routers import attendance, chat, auth, users, leave, settings
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

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
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 確保有 cache_buster 變數，沒有的話補上這行
    import time
    cache_buster = int(time.time())
    
    # 👇 重點是這行，把 request, name, context 清清楚楚地指派給它！
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"request": request, "version": cache_buster}
    )


@app.get("/api/health")
@app.head("/api/health") # 👈 新增這行，明確支援 HEAD 請求
def health_check(db: Session = Depends(get_db)):
    # 對 Supabase 下達一個最輕量的查詢指令
    db.execute(text("SELECT 1"))
    return {"status": "alive", "database": "connected"}