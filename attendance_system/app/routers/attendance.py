from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from typing import List, Optional

# 設定台灣時區 (UTC+8)
TW_TZ = timezone(timedelta(hours=8))

from app.database import get_db
from app.models import Attendance, User
from app.schemas import Attendance as AttendanceSchema

router = APIRouter()

@router.post("/", response_model=AttendanceSchema)
def check_in_or_update(employee_name: str, action: str, db: Session = Depends(get_db)):
    """
    更新或建立當日的打卡紀錄
    action 可為: 上班, 吃午餐, 午餐回來, 下班
    """
    if not employee_name.strip():
        raise HTTPException(status_code=400, detail="員工姓名不能為空")

    tw_now = datetime.now(TW_TZ)
    today = tw_now.date()
    now_time = tw_now.time()
    
    # 尋找今日是否已有該名員工的打卡紀錄
    record = db.query(Attendance).filter(
        Attendance.employee_name == employee_name,
        Attendance.date == today
    ).first()

    # 如果尚未有紀錄，則只允許「上班」動作
    if not record:
        if action != "上班":
            raise HTTPException(status_code=400, detail="今日尚未上班打卡，請先點擊上班！")
        
        record = Attendance(
            employee_name=employee_name,
            date=today,
            check_in_time=now_time,
            status="上班中"
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    # 若已有紀錄，則依照動作更新不同的時間欄位
    if action == "上班":
        raise HTTPException(status_code=400, detail="今日已經打過上班卡了！")
    elif action == "吃午餐":
        if record.lunch_out_time:
            raise HTTPException(status_code=400, detail="已經打過吃午餐了！")
        record.lunch_out_time = now_time
        record.status = "午休中"
    elif action == "午餐回來":
        if not record.lunch_out_time:
            raise HTTPException(status_code=400, detail="尚未打吃午餐，無法打午餐回來卡！")
        if record.lunch_in_time:
            raise HTTPException(status_code=400, detail="已經打過午餐回來了！")
        record.lunch_in_time = now_time
        record.status = "上班中"
    elif action == "下班":
        if record.check_out_time:
            raise HTTPException(status_code=400, detail="已經打過下班卡了！辛苦了！")
        record.check_out_time = now_time
        record.status = "已下班"
    else:
        raise HTTPException(status_code=400, detail="未知的打卡動作")

    db.commit()
    db.refresh(record)
    return record

@router.get("/today", response_model=List[AttendanceSchema])
def get_today_attendance(username: str, db: Session = Depends(get_db)):
    """取得所有人今天的打卡紀錄"""
    user = db.query(User).filter(User.username == username).first()
    if not user or user.role not in [1, 2]:
        raise HTTPException(status_code=403, detail="權限不足，僅限管理員或經理查詢")
    tw_now = datetime.now(TW_TZ)
    today = tw_now.date()
    records = db.query(Attendance).filter(Attendance.date == today).all()
    return records

@router.get("/search", response_model=List[AttendanceSchema])
def search_attendance(
    username: str, 
    start_date: str, 
    end_date: str, 
    target_employee_name: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="無效的帳號")
    
    try:
        start_d = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_d = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式錯誤，請使用 YYYY-MM-DD")
        
    query = db.query(Attendance).filter(Attendance.date >= start_d, Attendance.date <= end_d)
    
    if user.role in [1, 2]:
        if target_employee_name:
            query = query.filter(Attendance.employee_name == target_employee_name)
    else:
        query = query.filter(Attendance.employee_name == user.employee_name)
        
    records = query.order_by(Attendance.date.desc()).all()
    return records

@router.get("/{employee_name}", response_model=List[AttendanceSchema])
def get_attendance_records(employee_name: str, db: Session = Depends(get_db)):
    """取得某位員工的所有打卡歷史紀錄"""
    records = db.query(Attendance).filter(
        Attendance.employee_name == employee_name
    ).order_by(Attendance.date.desc()).all()
    return records
