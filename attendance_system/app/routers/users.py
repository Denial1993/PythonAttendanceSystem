from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserProfileUpdate

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


@router.get("/me", response_model=UserResponse)
def get_my_profile(username: str, db: Session = Depends(get_db)):
    """
    取得目前登入員工自己的個人詳細資料。
    任一登入角色皆可使用。
    """
    return _get_current_user_by_username(username, db)


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
