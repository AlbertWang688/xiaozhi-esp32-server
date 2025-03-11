#基于sqlmodel的userchatmemory表的增删改查操作
from sqlmodel import Session, select, and_, or_
from datetime import date
from backend.app.models.xiaozhi import UserChatMemory

class UserChatMemoryDAO:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, user_chat_memory: UserChatMemory) -> UserChatMemory:
        self.session.add(user_chat_memory)
        self.session.commit()
        self.session.refresh(user_chat_memory)
        return user_chat_memory

    async def get_by_id(self, ucm_nativeID: int) -> UserChatMemory:
        statement = select(UserChatMemory).where(UserChatMemory.ucm_nativeID == ucm_nativeID)
        return self.session.exec(statement).first()

    async def get_all_memories_ofUser(self,user_id: int) -> list[UserChatMemory]:
        statement = select(UserChatMemory).where(UserChatMemory.user.du_nativeID)
        return self.session.exec(statement).all()

    #获取某一时间期间的记忆
    async def get_memories_by_date_range(self,user_id: int, start_date: date, end_date: date) -> list[UserChatMemory]:
        statement = select(UserChatMemory).where(
            and_(
                UserChatMemory.du_nativeID == user_id,
                UserChatMemory.ucm_chatDate >= start_date, 
                UserChatMemory.ucm_chatDate <= end_date
            )
        )
        return self.session.exec(statement).all()
    async def update(self, ucm_nativeID: int, userchatmemory: UserChatMemory) -> UserChatMemory:
        user_chat_memory = self.get_by_id(ucm_nativeID)
        if user_chat_memory:
            for key, value in userchatmemory.items():
                setattr(user_chat_memory, key, value)
            self.session.commit()
            self.session.refresh(user_chat_memory)
        return user_chat_memory

    async def delete(self, ucm_nativeID: int) -> bool:
        user_chat_memory = self.get_by_id(ucm_nativeID)
        if user_chat_memory:
            self.session.delete(user_chat_memory)
            self.session.commit()
            return True
        return False
