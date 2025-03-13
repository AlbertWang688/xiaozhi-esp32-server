from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from datetime import datetime
from backend.app.models.xiaozhi import Device, DevUser, UserChatMemory, UserSession
from backend.app.dao.device import DeviceDAO
from backend.app.db import get_session
from backend.app.auth import verify_token,generate_token_for_device,get_current_device,TokenData

router = APIRouter()

# Device endpoints
@router.post("/", response_model=Device,description="新增设备")
async def create_device(device: Device, session: Session = Depends(get_session)):
    dao = DeviceDAO(session)
    # db_device = device.model_validate_json(device)
    return await dao.create(device)

@router.get("/{device_id}", response_model=Device,description="查询设备")
async def get_device(
    device_id: int, 
    session: Session = Depends(get_session),
    current_device: TokenData = Depends(get_current_device)
    ):
    dao = DeviceDAO(session)
    device = await dao.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=Device,description="更新设备")
async def update_device(
    device_id: int, 
    device: Device, 
    session: Session = Depends(get_session),
    current_device: TokenData = Depends(get_current_device)
    ):
    dao = DeviceDAO(session)
    updated_device = await dao.update(device_id, device)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

@router.delete("/{device_id}",description="删除设备")
async def delete_device(
    device_id: int, 
    session: Session = Depends(get_session),
    current_device: TokenData = Depends(get_current_device)
    ):
    dao = DeviceDAO(session)
    if not await dao.delete(device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}

