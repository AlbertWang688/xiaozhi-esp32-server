from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.app.dao.usersession import UserSessionDAO
from backend.app.models.xiaozhi import UserSession
from backend.app.db import get_session
from datetime import datetime

router = APIRouter()

@router.post("/usersessions/", response_model=UserSession)
async def create_user_session(user_session: UserSession, session: Session = Depends(get_session)):
    dao = UserSessionDAO(session)
    return await dao.create(user_session)

@router.get("/usersessions/{us_nativeid}", response_model=UserSession)
async def get_user_session(us_nativeid: int, session: Session = Depends(get_session)):
    dao = UserSessionDAO(session)
    user_session = await dao.get_by_id(us_nativeid)
    if not user_session:
        raise HTTPException(status_code=404, detail="User session not found")
    return user_session

@router.get("/usersessions/user/{user_id}", response_model=list[UserSession])
async def get_all_sessions_of_user(user_id: int, session: Session = Depends(get_session)):
    dao = UserSessionDAO(session)
    return await dao.get_all_sessions_of_user(user_id)

@router.get("/usersessions/user/{user_id}/date_range", response_model=list[UserSession])
async def get_sessions_by_date_range(user_id: int, start_date: datetime, end_date: datetime, session: Session = Depends(get_session)):
    dao = UserSessionDAO(session)
    return await dao.get_sessions_by_date_range(user_id, start_date, end_date)

@router.put("/usersessions/{us_nativeid}", response_model=UserSession)
async def update_user_session(us_nativeid: int, user_session: UserSession, session: Session = Depends(get_session)):
    dao = UserSessionDAO(session)
    updated_session = await dao.update(us_nativeid, user_session)
    if not updated_session:
        raise HTTPException(status_code=404, detail="User session not found")
    return updated_session

@router.delete("/usersessions/{us_nativeid}", response_model=bool)
async def delete_user_session(us_nativeid: int, session: Session = Depends(get_session)):
    dao = UserSessionDAO(session)
    success = await dao.delete(us_nativeid)
    if not success:
        raise HTTPException(status_code=404, detail="User session not found")
    return success