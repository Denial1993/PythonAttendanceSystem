from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.models import Holidays, LeaveBalances

def check_if_workday(date_obj: date, db: Session) -> bool:
    """檢查指定日期是否為工作日"""
    holiday_record = db.query(Holidays).filter(Holidays.date == date_obj).first()
    if holiday_record:
        # 國定假日 (is_holiday=True) -> 回傳 False (非工作日)
        # 補班日 (is_holiday=False) -> 回傳 True (是工作日)
        return not holiday_record.is_holiday
    
    # 若行事曆表沒有特別紀錄，預設六日放假
    if date_obj.weekday() >= 5: # 5 是星期六, 6 是星期日
        return False
        
    return True

def calculate_request_hours(start_dt: datetime, end_dt: datetime, db: Session) -> float:
    """計算請假區間內的實際工作小時數（跳過假日、扣除午休）"""
    total_hours = 0.0
    current_date = start_dt.date()
    end_date = end_dt.date()
    
    while current_date <= end_date:
        if check_if_workday(current_date, db):
            # 假設標準上班時間為 09:00 ~ 18:00
            day_start = datetime.combine(current_date, datetime.min.time())
            
            actual_start = start_dt if current_date == start_dt.date() else day_start.replace(hour=9, minute=0)
            actual_end = end_dt if current_date == end_dt.date() else day_start.replace(hour=18, minute=0)
            
            work_start = day_start.replace(hour=9, minute=0)
            work_end = day_start.replace(hour=18, minute=0)
            
            calc_start = max(actual_start, work_start)
            calc_end = min(actual_end, work_end)
            
            if calc_start < calc_end:
                hours = (calc_end - calc_start).total_seconds() / 3600.0
                
                # 扣除午休 12:00~13:00
                lunch_start = day_start.replace(hour=12, minute=0)
                lunch_end = day_start.replace(hour=13, minute=0)
                overlap_start = max(calc_start, lunch_start)
                overlap_end = min(calc_end, lunch_end)
                
                if overlap_start < overlap_end:
                    lunch_hours = (overlap_end - overlap_start).total_seconds() / 3600.0
                    hours -= lunch_hours
                    
                total_hours += hours
                
        current_date += timedelta(days=1)
        
    return total_hours

def check_leave_balance(user_id: int, leave_type: str, required_hours: float, ref_date: date, db: Session) -> bool:
    """檢查特定假別剩餘可用時數是否足夠"""
    # 事假病假如果不設上限或不需要事前分配，可直接回傳 True，
    # 這裡我們為了嚴謹，假設所有受控假別都必須有餘額，或者針對特休等。
    balance = db.query(LeaveBalances).filter(
        LeaveBalances.user_id == user_id,
        LeaveBalances.leave_type == leave_type,
        LeaveBalances.valid_from <= ref_date,
        LeaveBalances.valid_until >= ref_date
    ).first()
    
    if not balance:
        return False
        
    available = balance.total_hours - balance.used_hours
    return available >= required_hours

def deduct_leave_balance(user_id: int, leave_type: str, hours: float, ref_date: date, db: Session):
    """扣除特定假別的可用時數"""
    balance = db.query(LeaveBalances).filter(
        LeaveBalances.user_id == user_id,
        LeaveBalances.leave_type == leave_type,
        LeaveBalances.valid_from <= ref_date,
        LeaveBalances.valid_until >= ref_date
    ).first()
    
    if balance:
        balance.used_hours += hours
        db.commit()
