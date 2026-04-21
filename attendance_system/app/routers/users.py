from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserProfileUpdate
from pydantic import BaseModel
from app.models import LeaveBalances
from app.schemas import LeaveBalanceResponse
from datetime import date

# 定義前端傳過來的資料格式 (DTO)
class UserUpdateRequest(BaseModel):
    username: str
    phone: str = None
    address: str = None
    salary: int = None  # 👈 新增這行：允許接收薪水資料
    
router = APIRouter()

def _get_current_user_by_username(username: str, db: Session) -> User:
    """從 username 取得目前使用者，找不到則拋出 404"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="使用者不存在")
    return user


@router.get("", response_model=List[UserResponse])
def list_all_users(username: str, db: Session = Depends(get_db)):
    """
    取得所有員工的詳細資料列表（含電話、地址、薪資）。
    僅允許 Role 1 (Admin) 或 Role 2 (Manager) 呼叫。
    """
    current_user = _get_current_user_by_username(username, db)
    if current_user.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="權限不足，僅管理者可查看所有員工資料"
        )
    return db.query(User).order_by(User.id).all()

@router.get("/me")
def get_my_profile(username: str, db: Session = Depends(get_db)):
    """讀取自己的個人資料"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="找不到此使用者")
    
    return {
        "employee_name": user.employee_name, 
        "phone": user.phone, 
        "address": user.address, 
        "salary": user.salary
    }

@router.put("/me")
def update_my_profile(request: UserUpdateRequest, db: Session = Depends(get_db)):
    # 1. 去資料庫找這個人
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="找不到此使用者")

    # 2. 更新資料
    if request.phone is not None:
        user.phone = request.phone
    if request.address is not None:
        user.address = request.address
    if request.salary is not None:        # 👈 新增這兩行：把薪水存進資料庫
        user.salary = request.salary

    # 3. 存檔回資料庫
    db.commit()
    db.refresh(user)

    return {"message": "個人資料更新成功", "phone": user.phone, "address": user.address, "salary": user.salary}

@router.get("/me/leave_balances", response_model=List[LeaveBalanceResponse])
def get_my_leave_balances(username: str, db: Session = Depends(get_db)):
    """取得員工當下有效的各類假勤餘額"""
    user = _get_current_user_by_username(username, db)
    today = date.today()
    balances = db.query(LeaveBalances).filter(
        LeaveBalances.user_id == user.id,
        LeaveBalances.valid_from <= today,
        LeaveBalances.valid_until >= today
    ).all()
    return balances


@router.put("/{user_id}", response_model=UserResponse)
def update_user_profile(
    user_id: int,
    profile: UserProfileUpdate,
    username: str,
    db: Session = Depends(get_db)
):
    """
    更新指定員工的詳細資料（電話、地址、薪資）。
    僅允許 Role 1 (Admin) 或 Role 2 (Manager) 呼叫。
    """
    current_user = _get_current_user_by_username(username, db)
    if current_user.role not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="權限不足，僅管理者可修改員工資料"
        )

    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="指定的員工不存在")

    # 只更新有傳入的欄位（排除 None 的值）
    update_data = profile.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(target_user, field, value)

    db.commit()
    db.refresh(target_user)
    return target_user



