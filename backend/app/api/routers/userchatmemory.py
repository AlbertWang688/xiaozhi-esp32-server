from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.app.dao.userchatmemory import UserChatMemoryDAO
from backend.app.models.xiaozhi import UserChatMemory
from backend.app.db import get_session
from datetime import date

router = APIRouter()

@router.post("/userchatmemory/", response_model=UserChatMemory)
async def create_user_chat_memory(user_chat_memory: UserChatMemory, session: Session = Depends(get_session)):
    dao = UserChatMemoryDAO(session)
    return await dao.create(user_chat_memory)

@router.get("/userchatmemory/{ucm_nativeID}", response_model=UserChatMemory)
async def get_user_chat_memory(ucm_nativeID: int, session: Session = Depends(get_session)):
    dao = UserChatMemoryDAO(session)
    user_chat_memory = await dao.get_by_id(ucm_nativeID)
    if not user_chat_memory:
        raise HTTPException(status_code=404, detail="User chat memory not found")
    return user_chat_memory

@router.get("/userchatmemory/user/{user_id}", response_model=list[UserChatMemory])
async def get_all_memories_of_user(user_id: int, session: Session = Depends(get_session)):
    dao = UserChatMemoryDAO(session)
    return await dao.get_all_memories_ofUser(user_id)

@router.get("/userchatmemory/user/{user_id}/date_range", response_model=list[UserChatMemory])
async def get_memories_by_date_range(user_id: int, start_date: date, end_date: date, session: Session = Depends(get_session)):
    dao = UserChatMemoryDAO(session)
    return await dao.get_memories_by_date_range(user_id, start_date, end_date)

@router.put("/userchatmemory/{ucm_nativeID}", response_model=UserChatMemory)
async def update_user_chat_memory(ucm_nativeID: int, user_chat_memory: UserChatMemory, session: Session = Depends(get_session)):
    dao = UserChatMemoryDAO(session)
    updated_memory = await dao.update(ucm_nativeID, user_chat_memory)
    if not updated_memory:
        raise HTTPException(status_code=404, detail="User chat memory not found")
    return updated_memory

@router.delete("/userchatmemory/{ucm_nativeID}", response_model=bool)
async def delete_user_chat_memory(ucm_nativeID: int, session: Session = Depends(get_session)):
    dao = UserChatMemoryDAO(session)
    success = await dao.delete(ucm_nativeID)
    if not success:
        raise HTTPException(status_code=404, detail="User chat memory not found")
    return success