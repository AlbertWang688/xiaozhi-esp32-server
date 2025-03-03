from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from crud import crud
from pydantic import BaseModel
from datetime import date, datetime

app = FastAPI()

# Pydantic模型
class DevUserBase(BaseModel):
    du_userAccount: str
    du_userName: str
    du_sex: str
    du_birthday: date
    du_age: int
    du_mobilPhone: str
    du_userIntro: str
    d_nativeID: int

class DeviceBase(BaseModel):
    d_devMac: str
    d_regStatus: str
    d_bindDate: datetime
    d_appToken: str
    d_protocalVersion: str
    d_configJson: str

# API路由
@app.post("/users/", response_model=DevUserBase)
def create_user(user: DevUserBase, db: Session = Depends(get_db)):
    return crud.create_dev_user(db, user.dict())

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_dev_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: DevUserBase, db: Session = Depends(get_db)):
    db_user = crud.update_dev_user(db, user_id, user.dict())
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_dev_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Device API路由
@app.post("/devices/", response_model=DeviceBase)
def create_device(device: DeviceBase, db: Session = Depends(get_db)):
    return crud.create_device(db, device.dict())

@app.get("/devices/{device_id}")
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device 