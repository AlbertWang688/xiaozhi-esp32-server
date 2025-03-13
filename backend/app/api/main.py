from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
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
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

app.include_router(device.router,prefix="/devices",tags=["设备管理"])
app.include_router(devuser.router,prefix="/devusers",tags=["设备用户管理"])
app.include_router(userchatmemory.router,prefix="/userchatmemories",tags=["用户聊天记录管理"])
app.include_router(usersession.router,prefix="/usersessions",tags=["用户会话管理"]) 

#检查设备mac和激活码是否匹配
def check_device_valid(mac: str, activation_code: str=None) -> bool:
    # Implement your logic to check if the provided mac and activation code match
    # Return True if they match, False otherwise
    return True

# Token generation endpoint
@app.get("/token", description="生成设备Token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     d_dev_mac = form_data.d_dev_mac
#     d_activation_code = form_data.d_activation_code
#     token = generate_token_for_device(d_dev_mac, d_activation_code)
#     return {"access_token": token, "token_type": "bearer"}
async def get_token(
    d_dev_mac: str, 
    d_activation_code: str=None,
    session:AsyncSession=Depends(get_session)
):
    # if not check_device_valid(d_dev_mac, d_activation_code):
    #     raise HTTPException(status_code=401, detail="Invalid device mac or activation code")
    token = await generate_token_for_device(d_dev_mac, d_activation_code,session)
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.api.main:app", host="0.0.0.0", port=8001,reload=True)