from sqlalchemy import Column, Integer, String, DateTime, Date, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class DevUser(Base):
    __tablename__ = "xz_devUser"
    
    du_nativeID = Column(BigInteger, primary_key=True)
    d_nativeID = Column(BigInteger, ForeignKey('xz_device.d_nativeID'))
    du_userAccount = Column(String(50))
    du_userName = Column(String(50))
    du_sex = Column(String(1))
    du_birthday = Column(Date)
    du_age = Column(Integer)
    du_mobilPhone = Column(String(20))
    du_userIntro = Column(String(200))
    du_chatSummary = Column(String(2048))
    du_voicePrintFilePath = Column(String(100))
    du_createtime = Column(DateTime, default=datetime.now)
    du_updatetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    device = relationship("Device", back_populates="users")
    chat_memories = relationship("UserChatMemory", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")

class Device(Base):
    __tablename__ = "xz_device"
    
    d_nativeID = Column(BigInteger, primary_key=True)
    d_devMac = Column(String(50))
    d_regStatus = Column(String(1))
    d_bindDate = Column(DateTime)
    d_appToken = Column(String(100))
    d_protocalVersion = Column(String(10))
    d_configJson = Column(Text)

    users = relationship("DevUser", back_populates="device")

class UserChatMemory(Base):
    __tablename__ = "xz_userChatMemory"
    
    ucm_nativeID = Column(BigInteger, primary_key=True)
    du_nativeID = Column(BigInteger, ForeignKey('xz_devUser.du_nativeID'))
    ucm_chatDate = Column(Date)
    ucm_chatSummary = Column(String(1000))
    ucm_createtime = Column(DateTime, default=datetime.now)
    ucm_updateTime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("DevUser", back_populates="chat_memories")

class UserSession(Base):
    __tablename__ = "xz_userSession"
    
    us_nativeid = Column(Integer, primary_key=True)
    du_nativeID = Column(BigInteger, ForeignKey('xz_devUser.du_nativeID'))
    us_sessionid = Column(String(50))
    us_bgntime = Column(DateTime)
    us_endtime = Column(DateTime)
    us_content = Column(Text)

    user = relationship("DevUser", back_populates="sessions") 