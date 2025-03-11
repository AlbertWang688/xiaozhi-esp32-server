from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class DeviceBase(SQLModel):
    d_devMac: Optional[str] = Field(default=None, description="设备mac")
    d_activationCode: Optional[str] = Field(default=None, description="设备激活码")
    d_registerTime: Optional[datetime] = Field(description="注册时间",default_factory=datetime.now)
    d_regStatus: Optional[str] = Field(default=None, description="注册状态 0:未注册，1:已注册")
    d_appToken: Optional[str] = Field(default=None)
    d_protocalVersion: Optional[str] = Field(default=None)
    d_createTime: Optional[datetime] = Field(default_factory=datetime.now)
    d_updateTime: Optional[datetime] = Field(default_factory=datetime.now)
    d_robotNickName: Optional[str] = Field(default=None)
    d_voiceName: Optional[str] = Field(default=None)
    d_roleIntro: Optional[str] = Field(default=None)

class Device(DeviceBase, table=True):
    __tablename__ = "xz_device"
    d_nativeID: Optional[int] = Field(default=None, primary_key=True)
    users: list["DevUser"] = Relationship(back_populates="device")

class DevUserBase(SQLModel):
    d_nativeID: Optional[int] = Field(default=None, foreign_key="xz_device.d_nativeID")
    du_userAccount: Optional[str] = None
    du_userName: Optional[str] = None
    du_nickName: Optional[str] = None
    du_sex: Optional[str] = None
    du_birthday: Optional[date] = None
    du_age: Optional[int] = None
    du_mobilPhone: Optional[str] = None
    du_userIntro: Optional[str] = None
    du_chatSummary: Optional[str] = None
    du_voicePrintFilePath: Optional[str] = None
    du_createtime: datetime = Field(default_factory=datetime.now)
    du_updatetime: datetime = Field(default_factory=datetime.now)

class DevUser(DevUserBase, table=True):
    __tablename__ = "xz_devUser"
    du_nativeID: Optional[int] = Field(default=None, primary_key=True)
    device: Device = Relationship(back_populates="users")
    chat_memories: list["UserChatMemory"] = Relationship(back_populates="user")
    sessions: list["UserSession"] = Relationship(back_populates="user")

class UserChatMemoryBase(SQLModel):
    du_nativeID: Optional[int] = Field(default=None, foreign_key="xz_devUser.du_nativeID")
    ucm_chatDate: Optional[date] = None
    ucm_chatSummary: Optional[str] = None
    ucm_createtime: datetime = Field(default_factory=datetime.now)
    ucm_updateTime: datetime = Field(default_factory=datetime.now)

class UserChatMemory(UserChatMemoryBase, table=True):
    __tablename__ = "xz_userChatMemory"
    ucm_nativeID: Optional[int] = Field(default=None, primary_key=True)
    user: DevUser = Relationship(back_populates="chat_memories")

class UserSessionBase(SQLModel):
    du_nativeID: Optional[int] = Field(default=None, foreign_key="xz_devUser.du_nativeID")
    us_sessionid: str
    us_bgntime: Optional[datetime] = None
    us_endtime: Optional[datetime] = None
    us_content: Optional[str] = None

class UserSession(UserSessionBase, table=True):
    __tablename__ = "xz_userSession"
    us_nativeid: Optional[int] = Field(default=None, primary_key=True)
    user: DevUser = Relationship(back_populates="sessions") 