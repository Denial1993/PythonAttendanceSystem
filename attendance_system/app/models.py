from sqlalchemy import Column, Integer, String, Date, Time
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    employee_name = Column(String, nullable=False)
    role = Column(Integer, default=3)  # 1: admin, 2: manager, 3: normal


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
