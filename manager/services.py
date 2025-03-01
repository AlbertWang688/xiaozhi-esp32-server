# services.py
from sqlalchemy.orm import Session
from models import DevUser, Device, UserChatMemory, UserSession

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data):
        user = DevUser(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id):
        return self.db.query(DevUser).filter(DevUser.du_nativeID == user_id).first()

    # 其他业务逻辑方法...