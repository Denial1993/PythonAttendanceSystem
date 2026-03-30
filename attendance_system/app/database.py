import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# 從環境變數取得資料庫連線字串，若無則提供預設值（方便本機測試）
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://attendance_user:attendance_password@localhost:5432/attendance_db"
)

# 建立 SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 建立 SessionLocal 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 宣告 Base，所有的 Model 都要繼承這個類別
Base = declarative_base()

# FastAPI 依賴性注入用的 Generator
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
