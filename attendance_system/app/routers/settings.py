from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import SystemSettings, User
from app.schemas import SystemSettingsResponse, SystemSettingsUpdate

router = APIRouter()

def verify_admin(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.role != 1:
        raise HTTPException(status_code=403, detail="權限不足，僅限最高管理員操作")
    return user

@router.get("/", response_model=List[SystemSettingsResponse])
def get_settings(username: str, db: Session = Depends(get_db)):
    """取得所有系統設定"""
    verify_admin(username, db)
    settings = db.query(SystemSettings).all()
    return settings

@router.get("/{setting_key}", response_model=SystemSettingsResponse)
def get_setting_by_key(setting_key: str, db: Session = Depends(get_db)):
    """可以給前台不用權限讀取，或者需要的話加上權限"""
    # 這裡讓大家都能讀取基準點，以便前端計算或畫地圖
    setting = db.query(SystemSettings).filter(SystemSettings.setting_key == setting_key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="找不到該設定")
    return setting

@router.post("/{setting_key}", response_model=SystemSettingsResponse)
def update_setting(setting_key: str, update_data: SystemSettingsUpdate, username: str, db: Session = Depends(get_db)):
    """更新系統設定"""
    verify_admin(username, db)
    setting = db.query(SystemSettings).filter(SystemSettings.setting_key == setting_key).first()
    
    if not setting:
        # 如果不存在就建立
        setting = SystemSettings(setting_key=setting_key, setting_value=update_data.setting_value)
        db.add(setting)
    else:
        setting.setting_value = update_data.setting_value
        
    db.commit()
    db.refresh(setting)
    return setting
