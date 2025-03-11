from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from backend.app.models.xiaozhi import Device, DevUser, UserChatMemory, UserSession
from backend.app.dao.devuser import DevUserDAO
from backend.app.db import get_session

router = APIRouter()

# DevUser endpoints
@router.post("/", response_model=DevUser,description="新增设备用户")
async def create_user(user: DevUser, session: Session = Depends(get_session)):
    dao = DevUserDAO(session)
    return await dao.create(user)

@router.get("/{user_id}", response_model=DevUser,description="查询设备用户")
async def get_user(user_id: int, session: Session = Depends(get_session)):
    dao = DevUserDAO(session)
    user = await dao.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=DevUser,description="更新设备用户")
async def update_user(user_id: int, user: DevUser, session: Session = Depends(get_session)):
    dao = DevUserDAO(session)
    updated_user = await dao.update(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}",description="删除设备用户")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    dao = DevUserDAO(session)
    if not await dao.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"} 