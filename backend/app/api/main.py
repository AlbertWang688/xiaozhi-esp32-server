from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from backend.app.models.xiaozhi import Device, DevUser, UserChatMemory, UserSession
from backend.app.dao.devuser import DevUserDAO
from backend.app.dao.userchatmemory import UserChatMemoryDAO
from backend.app.dao.device import DeviceDAO
# from backend.app.dao.usersession import UserSessionDAO
from backend.app.db import get_session
from backend.app.api.routers import device,devuser,userchatmemory,usersession
from backend.app.auth import verify_token,generate_token_for_device,get_current_device,TokenData


app = FastAPI()

app.include_router(device.router,prefix="/devices",tags=["设备管理"])
app.include_router(devuser.router,prefix="/devusers",tags=["设备用户管理"])
app.include_router(userchatmemory.router,prefix="/userchatmemories",tags=["用户聊天记录管理"])
app.include_router(usersession.router,prefix="/usersessions",tags=["用户会话管理"]) 
# Token generation endpoint
@app.get("/generate_token", description="生成设备Token")
async def generate_token(dev_mac: str):
    token = generate_token_for_device(dev_mac)
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.api.main:app", host="0.0.0.0", port=8001,reload=True)