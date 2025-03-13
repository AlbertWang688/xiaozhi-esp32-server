from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from backend.app.models.xiaozhi import Device, DevUser, UserChatMemory, UserSession
from backend.app.dao.devuser import DevUserDAO
from backend.app.db import get_session
from backend.app.auth import get_current_device, TokenData
from fastapi import File, UploadFile

router = APIRouter()

# DevUser endpoints
@router.post("/", response_model=DevUser,description="新增设备用户")
async def create_user(
    user: DevUser,
    session: Session = Depends(get_session),
    current_device: TokenData = Depends(get_current_device)
    ):
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

#上传并更新设备用户的声纹文件
@router.post("/upload_voiceprint/{user_id}",description="上传并更新设备用户的声纹文件")
async def upload_voiceprint(
    user_id: int, 
    file: UploadFile = File(...), 
    session: Session = Depends(get_session),
    current_device: TokenData = Depends(get_current_device)
    ):
    dao = DevUserDAO(session)
    user = await dao.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Save the uploaded file
    voiceprint_file = f"voiceprint_{user_id}.wav"
    with open(voiceprint_file, "wb") as f:
        f.write(file.file.read())
    # Update the user with the voiceprint file
    user.du_voiceprint = voiceprint_file
    await dao.update(user_id, user)
    return {"message": "Voiceprint file uploaded successfully"}