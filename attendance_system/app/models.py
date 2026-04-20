from sqlalchemy import Column, Integer, String, Date, Time, Float, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="自動增量 ID")
    username = Column(String, unique=True, index=True, nullable=False, comment="登入帳號/工號")
    password_hash = Column(String, nullable=False, comment="加密後的密碼")
    employee_name = Column(String, nullable=False, comment="員工真實姓名")
    role = Column(Integer, default=3, comment="權限角色 (1: admin, 2: manager, 3: normal)")
    phone = Column(String, nullable=True, comment="聯絡電話")
    address = Column(String, nullable=True, comment="居住地址")
    salary = Column(Integer, nullable=True, comment="月薪 (新台幣)")
    hire_date = Column(Date, nullable=True, comment="到職日 (用於計算特休週年制)")


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, comment="打卡紀錄 ID")
    employee_name = Column(String, index=True, nullable=False, comment="員工姓名")
    date = Column(Date, index=True, nullable=False, comment="打卡日期")
    check_in_time = Column(Time, nullable=True, comment="上班打卡時間")
    lunch_out_time = Column(Time, nullable=True, comment="午休開始時間")
    lunch_in_time = Column(Time, nullable=True, comment="午休結束時間")
    check_out_time = Column(Time, nullable=True, comment="下班打卡時間")
    check_in_lat = Column(Float, nullable=True, comment="上班打卡緯度")
    check_in_lng = Column(Float, nullable=True, comment="上班打卡經度")
    check_out_lat = Column(Float, nullable=True, comment="下班打卡緯度")
    check_out_lng = Column(Float, nullable=True, comment="下班打卡經度")
    status = Column(String, default="尚未上班", comment="目前打卡狀態 (例如: 上班中、已下班)")

class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String, unique=True, index=True, nullable=False, comment="設定鍵名")
    setting_value = Column(String, nullable=True, comment="設定值")
    description = Column(String, nullable=True, comment="說明")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True, comment="假單 ID")
    user_id = Column(Integer, index=True, nullable=False, comment="申請人的 User ID")
    leave_type = Column(String, nullable=False, comment="假別 (例如: 事假, 病假, 特休)")
    start_time = Column(String, nullable=False, comment="請假開始時間 (ISO 8601格式)")
    end_time = Column(String, nullable=False, comment="請假結束時間 (ISO 8601格式)")
    reason = Column(String, nullable=True, comment="請假事由")
    status = Column(String, default="pending", comment="審核狀態 (pending, approved, rejected)")
    created_at = Column(String, nullable=False, comment="假單建立時間")
    updated_at = Column(String, nullable=False, comment="假單最後更新時間")

class Holidays(Base):
    __tablename__ = "holidays"

    date = Column(Date, primary_key=True, index=True, comment="日期")
    name = Column(String, nullable=False, comment="節日或補班日名稱")
    is_holiday = Column(Boolean, default=True, comment="是否為放假日 (True: 放假, False: 補班照常上班)")

class LeaveBalances(Base):
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False, comment="員工 ID")
    leave_type = Column(String, nullable=False, comment="假別 (例如: 特休, 事假, 病假)")
    total_hours = Column(Float, nullable=False, default=0.0, comment="總時數")
    used_hours = Column(Float, nullable=False, default=0.0, comment="已用時數")
    valid_from = Column(Date, nullable=False, comment="生效日")
    valid_until = Column(Date, nullable=False, comment="失效日")