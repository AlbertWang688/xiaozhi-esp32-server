from sqlmodel import Session, select, and_, or_
from datetime import datetime
from backend.app.models.xiaozhi import UserSession

class UserSessionDAO:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, user_session: UserSession) -> UserSession:
        self.session.add(user_session)
        self.session.commit()
        self.session.refresh(user_session)
        return user_session

    async def get_by_id(self, us_nativeid: int) -> UserSession:
        statement = select(UserSession).where(UserSession.us_nativeid == us_nativeid)
        return self.session.exec(statement).first()

    async def get_all_sessions_of_user(self, user_id: int) -> list[UserSession]:
        statement = select(UserSession).where(UserSession.du_nativeID == user_id)
        return self.session.exec(statement).all()

    async def get_sessions_by_date_range(self, user_id: int, start_date: datetime, end_date: datetime) -> list[UserSession]:
        statement = select(UserSession).where(
            and_(
                UserSession.du_nativeID == user_id,
                UserSession.us_bgntime >= start_date,
                UserSession.us_endtime <= end_date
            )
        )
        return self.session.exec(statement).all()

    async def update(self, us_nativeid: int, user_session: UserSession) -> UserSession:
        existing_session = self.get_by_id(us_nativeid)
        if existing_session:
            for key, value in user_session.dict(exclude_unset=True).items():
                setattr(existing_session, key, value)
            self.session.commit()
            self.session.refresh(existing_session)
        return existing_session

    async def delete(self, us_nativeid: int) -> bool:
        user_session = self.get_by_id(us_nativeid)
        if user_session:
            self.session.delete(user_session)
            self.session.commit()
            return True
        return False