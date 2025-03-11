from sqlmodel import Session, select
from typing import List, Optional
from backend.app.models.xiaozhi import Device, DevUser, UserSession


class DevUserDAO:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, user: DevUser) -> DevUser:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[DevUser]:
        return self.session.get(DevUser, user_id)

    async def get_by_account(self, account: str) -> Optional[DevUser]:
        statement = select(DevUser).where(DevUser.du_userAccount == account)
        return self.session.exec(statement).first()

    async def update(self, user_id: int, user: DevUser) -> Optional[DevUser]:
        db_user = await self.get_by_id(user_id)
        if not db_user:
            return None
        
        user_data = user.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True 