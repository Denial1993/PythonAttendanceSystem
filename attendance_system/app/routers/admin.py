from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import date

from app.database import get_db
from app import models

router = APIRouter()


@router.get("/create")
def create_page():
    return {"message": "這是建立頁面"}


@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()

    # ── 區塊一：今日數字卡片 ──────────────────────────────

    # 系統裡的總員工數（role=3 是一般員工，但這裡先算全部）
    total_employees = db.query(func.count(models.User.id)).scalar()

    # 今日有打上班卡的人數
    checked_in_today = (
        db.query(func.count(models.Attendance.id))
        .filter(models.Attendance.date == today)
        .scalar()
    )

    # 今日請假且審核通過的人數
    # leave_requests 的 start_time 是字串 (ISO 8601)，用 LIKE 比對日期部分
    on_leave_today = (
        db.query(func.count(models.LeaveRequest.id))
        .filter(
            models.LeaveRequest.status == "approved",
            models.LeaveRequest.start_time.like(f"{today}%"),
        )
        .scalar()
    )

    # ── 區塊二：本月每日出勤人數（折線圖用）────────────────

    # 取得本月所有出勤紀錄，以日期分組計算人數
    monthly_raw = (
        db.query(
            models.Attendance.date,
            func.count(models.Attendance.id).label("count"),
        )
        .filter(
            models.Attendance.date >= date(today.year, today.month, 1),
            models.Attendance.date <= today,
        )
        .group_by(models.Attendance.date)
        .order_by(models.Attendance.date)
        .all()
    )

    monthly_attendance = [
        {"date": str(row.date), "count": row.count}
        for row in monthly_raw
    ]

    # ── 區塊三：假別申請分佈（圓餅圖用）────────────────────

    leave_raw = (
        db.query(
            models.LeaveRequest.leave_type,
            func.count(models.LeaveRequest.id).label("count"),
        )
        .filter(models.LeaveRequest.status == "approved")
        .group_by(models.LeaveRequest.leave_type)
        .all()
    )

    leave_distribution = [
        {"name": row.leave_type, "value": row.count}
        for row in leave_raw
    ]

    # ── 組合回傳 ─────────────────────────────────────────

    return {
        "today_stats": {
            "total_employees": total_employees,
            "checked_in_today": checked_in_today,
            "on_leave_today": on_leave_today,
        },
        "monthly_attendance": monthly_attendance,
        "leave_distribution": leave_distribution,
    }