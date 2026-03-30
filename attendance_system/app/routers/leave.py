from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("", response_model=schemas.LeaveRequestResponse)
def create_leave_request(
    request: schemas.LeaveRequestCreate,
    username: str, # 用 username 查詢當前操作人 (Role 3)
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_leave = models.LeaveRequest(
        user_id=user.id,
        leave_type=request.leave_type,
        start_time=request.start_time,
        end_time=request.end_time,
        reason=request.reason,
        status="pending",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    
    # 轉換成 Response 格式
    resp = schemas.LeaveRequestResponse.model_validate(new_leave)
    resp.employee_name = user.employee_name
    return resp

@router.get("", response_model=List[schemas.LeaveRequestResponse])
def get_leave_requests(
    username: str, # 用 username 辨識身份
    db: Session = Depends(get_db)
):
    current_user = db.query(models.User).filter(models.User.username == username).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    query = db.query(models.LeaveRequest, models.User).join(models.User, models.LeaveRequest.user_id == models.User.id)
    
    if current_user.role == 3:
        # 一般員工只能看自己的假單
        query = query.filter(models.LeaveRequest.user_id == current_user.id)
    # Role 1 & 2 不做 filter 就是看全部
    
    query = query.order_by(models.LeaveRequest.created_at.desc())
    results = query.all()
    
    # 整理回傳結構
    response_list = []
    for leave_reg, usr in results:
        r = schemas.LeaveRequestResponse.model_validate(leave_reg)
        r.employee_name = usr.employee_name
        response_list.append(r)
        
    return response_list

@router.put("/{leave_id}/status", response_model=schemas.LeaveRequestResponse)
def update_leave_status(
    leave_id: int,
    request: schemas.LeaveRequestUpdateStatus,
    username: str,
    db: Session = Depends(get_db)
):
    current_user = db.query(models.User).filter(models.User.username == username).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role not in [1, 2]:
        raise HTTPException(status_code=403, detail="Permission denied")
        
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
        
    leave.status = request.status
    leave.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db.commit()
    db.refresh(leave)
    
    # 取出對應員工姓名
    usr = db.query(models.User).filter(models.User.id == leave.user_id).first()
    
    resp = schemas.LeaveRequestResponse.model_validate(leave)
    resp.employee_name = usr.employee_name if usr else "未知"
    return resp
