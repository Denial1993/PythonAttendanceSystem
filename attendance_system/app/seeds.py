"""
seeds.py — 種子資料模組

設計原則（冪等性）：
  每次執行都會先檢查資料是否已存在，若已存在則跳過，
  不會產生重複資料，可安全地在每次應用啟動時呼叫。

包含的種子資料：
  1. 預設帳號（管理員 × 1、主管 × 1、一般員工 × 1）
  2. 系統設定初始值（公司位置座標、打卡範圍）
  3. 預設帳號的 2026 年請假額度
"""

from datetime import date
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User, SystemSettings, LeaveBalances
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─────────────────────────────────────────────
# 種子資料定義
# ─────────────────────────────────────────────

# 預設帳號
# 角色規則（與 auth.py 的 register 邏輯保持一致）：
#   username 開頭 AD → role 1 (Admin)
#   username 開頭 MA → role 2 (Manager)
#   其餘               → role 3 (Employee)
SEED_USERS = [
    {
        "username":      "AD001",
        "password":      "admin@2026",
        "employee_name": "系統管理員",
        "role":          1,
        "phone":         "0900000001",
        "address":       "台北市信義區市府路1號",
        "salary":        80000,
        "hire_date":     date(2020, 1, 1),
    },
    {
        "username":      "MA001",
        "password":      "manager@2026",
        "employee_name": "預設主管",
        "role":          2,
        "phone":         "0900000002",
        "address":       "台北市大安區復興南路1號",
        "salary":        65000,
        "hire_date":     date(2021, 3, 1),
    },
    {
        "username":      "EM001",
        "password":      "employee@2026",
        "employee_name": "預設員工",
        "role":          3,
        "phone":         "0900000003",
        "address":       "新北市板橋區文化路1號",
        "salary":        40000,
        "hire_date":     date(2022, 6, 1),
    },
]

# 系統設定初始值
SEED_SETTINGS = [
    {
        "setting_key":   "company_lat",
        "setting_value": "25.0330",
        "description":   "公司所在地緯度（預設：台北101附近）",
    },
    {
        "setting_key":   "company_lng",
        "setting_value": "121.5654",
        "description":   "公司所在地經度（預設：台北101附近）",
    },
    {
        "setting_key":   "checkin_radius_meters",
        "setting_value": "300",
        "description":   "允許打卡的最大範圍（公尺）",
    },
]

# 請假額度（只套用在種子帳號、2026 整年）
SEED_LEAVE_BALANCES = [
    # leave_type, total_hours
    ("特休",  80.0),
    ("事假", 112.0),
    ("病假", 112.0),
]


# ─────────────────────────────────────────────
# 執行函式（各自冪等）
# ─────────────────────────────────────────────

def seed_users(db: Session):
    for data in SEED_USERS:
        existing = db.query(User).filter(User.username == data["username"]).first()
        if existing:
            print(f"  [SKIP] 使用者 '{data['username']}' 已存在")
            continue

        user = User(
            username      = data["username"],
            password_hash = pwd_context.hash(data["password"]),
            employee_name = data["employee_name"],
            role          = data["role"],
            phone         = data["phone"],
            address       = data["address"],
            salary        = data["salary"],
            hire_date     = data["hire_date"],
        )
        db.add(user)
        db.flush()  # 取得 user.id 供後續使用

        # 同步建立請假額度
        for leave_type, total_hours in SEED_LEAVE_BALANCES:
            lb = LeaveBalances(
                user_id     = user.id,
                leave_type  = leave_type,
                total_hours = total_hours,
                used_hours  = 0.0,
                valid_from  = date(2026, 1, 1),
                valid_until = date(2026, 12, 31),
            )
            db.add(lb)

        print(f"  [OK]   建立使用者 '{data['username']}' ({data['employee_name']})")

    db.commit()


def seed_settings(db: Session):
    for data in SEED_SETTINGS:
        existing = db.query(SystemSettings).filter(
            SystemSettings.setting_key == data["setting_key"]
        ).first()
        if existing:
            print(f"  [SKIP] 系統設定 '{data['setting_key']}' 已存在")
            continue

        setting = SystemSettings(
            setting_key   = data["setting_key"],
            setting_value = data["setting_value"],
            description   = data["description"],
        )
        db.add(setting)
        print(f"  [OK]   建立系統設定 '{data['setting_key']}' = {data['setting_value']}")

    db.commit()


# ─────────────────────────────────────────────
# 主要進入點
# ─────────────────────────────────────────────

def run_seeds():
    """執行所有種子資料，可安全地在應用程式啟動時呼叫（冪等）。"""
    print("=== [Seeds] 開始執行種子資料 ===")
    db = SessionLocal()
    try:
        print("--- 使用者與請假額度 ---")
        seed_users(db)
        print("--- 系統設定 ---")
        seed_settings(db)
        print("=== [Seeds] 種子資料執行完畢 ===")
    except Exception as e:
        import traceback
        print(f"[Seeds] 執行失敗：{e}")
        print(traceback.format_exc())
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
