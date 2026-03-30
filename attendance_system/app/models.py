from sqlalchemy import Column, Integer, String, Date, Time
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    employee_name = Column(String, nullable=False)
    role = Column(Integer, default=3)  # 1: admin, 2: manager, 3: normal
    phone = Column(String, nullable=True)     # 電話
    address = Column(String, nullable=True)   # 地址
    salary = Column(Integer, nullable=True)   # 月薪 (元)


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    check_in_time = Column(Time, nullable=True)
    lunch_out_time = Column(Time, nullable=True)
    lunch_in_time = Column(Time, nullable=True)
    check_out_time = Column(Time, nullable=True)
    status = Column(String, default="尚未上班")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    leave_type = Column(String, nullable=False) # e.g. 假別: 事假, 病假, 特休
    start_time = Column(String, nullable=False) # e.g. "2023-10-01T09:00"
    end_time = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

