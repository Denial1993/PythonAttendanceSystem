from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, time

class UserCreate(BaseModel):
    username: str
    password: str
    employee_name: str
    role: int = 3
    hire_date: Optional[date] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    employee_name: str
    role: int
    phone: Optional[str] = None
    address: Optional[str] = None
    salary: Optional[int] = None
    hire_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

class UserProfileUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    salary: Optional[int] = None
    hire_date: Optional[date] = None

class AttendanceBase(BaseModel):
    employee_name: str
    date: date

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdateStatus(BaseModel):
    action: str # "上班", "吃午餐", "午餐回來", "下班"

class Attendance(AttendanceBase):
    id: int
    check_in_time: Optional[time] = None
    lunch_out_time: Optional[time] = None
    lunch_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    check_in_lat: Optional[float] = None
    check_in_lng: Optional[float] = None
    check_out_lat: Optional[float] = None
    check_out_lng: Optional[float] = None
    status: str

    model_config = ConfigDict(from_attributes=True)

class AttendanceDailyDetail(BaseModel):
    """每日出勤明細"""
    date: date
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    is_late: bool = False
    late_minutes: int = 0
    is_missing_checkin: bool = False   # 有記錄但漏打上班卡
    is_missing_checkout: bool = False  # 有記錄但漏打下班卡

class AttendanceMonthlySummary(BaseModel):
    """月份出勤統計摘要"""
    year: int
    month: int
    work_days: int           # 本月出勤天數（有打卡記錄的天數）
    late_count: int          # 遲到次數
    total_late_minutes: int  # 遲到總分鐘數
    missing_checkin_days: int   # 缺打上班卡天數
    missing_checkout_days: int  # 缺打下班卡天數
    daily_details: List[AttendanceDailyDetail]

# === 假單管理相關 ===
class LeaveRequestCreate(BaseModel):
    leave_type: str
    start_time: str
    end_time: str
    reason: Optional[str] = None

class LeaveRequestUpdateStatus(BaseModel):
    status: str # "approved" 或 "rejected"

class LeaveRequestResponse(BaseModel):
    id: int
    user_id: int
    employee_name: Optional[str] = None # 用於前端顯示申請人姓名
    leave_type: str
    start_time: str
    end_time: str
    reason: Optional[str] = None
    status: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)

# === 系統設定相關 ===
class SystemSettingsBase(BaseModel):
    setting_key: str
    setting_value: Optional[str] = None
    description: Optional[str] = None

class SystemSettingsResponse(SystemSettingsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SystemSettingsUpdate(BaseModel):
    setting_value: Optional[str] = None

# === 假勤餘額與行事曆相關 ===
class LeaveBalanceBase(BaseModel):
    leave_type: str
    total_hours: float
    used_hours: float
    valid_from: date
    valid_until: date

class LeaveBalanceResponse(LeaveBalanceBase):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

class HolidayBase(BaseModel):
    date: date
    name: str
    is_holiday: bool

class HolidayResponse(HolidayBase):
    model_config = ConfigDict(from_attributes=True)
