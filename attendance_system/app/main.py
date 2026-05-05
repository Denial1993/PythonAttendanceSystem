from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import time

from app.database import engine, Base
from app.routers import attendance, chat, auth, users, leave, settings, admin
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

# 啟動時自動建立所有的資料庫表格
Base.metadata.create_all(bind=engine)

# 啟動時自動執行種子資料（冪等，已存在則跳過）
from app.seeds import run_seeds
run_seeds()

app = FastAPI(title="Attendance System", version="1.0.0")

# CORS Middleware（開發期允許 Vite dev server 跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 掛載靜態檔案目錄（main.js 等舊有靜態資源，保留相容）
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 設定模板目錄（保留 Jinja2 以便回退）
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# 掛載 Vue 建置產出的靜態資源（生產環境）
vue_dist_dir = os.path.join(os.path.dirname(__file__), "static", "dist")
if os.path.isdir(vue_dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(vue_dist_dir, "assets")), name="vue_assets")

# 註冊 API 路由（前綴均為 /api，與 axios baseURL 對應）
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(leave.router, prefix="/api/leave", tags=["Leave"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/api/health")
@app.head("/api/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "alive", "database": "connected"}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 生產環境：提供 Vue SPA 的 index.html
    vue_index = os.path.join(vue_dist_dir, "index.html")
    if os.path.isfile(vue_index):
        return FileResponse(vue_index)
    # 開發回退：Jinja2 舊模板
    cache_buster = int(time.time())
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "version": cache_buster}
    )


# SPA catch-all：讓 Vue Router (hash mode) 的任何路徑都回傳 index.html
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def spa_fallback(request: Request, full_path: str):
    # 不攔截 /api 與 /static 路徑
    if full_path.startswith("api/") or full_path.startswith("static/") or full_path.startswith("assets/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    vue_index = os.path.join(vue_dist_dir, "index.html")
    if os.path.isfile(vue_index):
        return FileResponse(vue_index)
    cache_buster = int(time.time())
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "version": cache_buster}
    )


