from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time

class UserCreate(BaseModel):
    username: str
    password: str
    employee_name: str
    role: int = 3

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    employee_name: str
    role: int

    model_config = ConfigDict(from_attributes=True)

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
    status: str

    model_config = ConfigDict(from_attributes=True)
