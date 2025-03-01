# models.py
from sqlalchemy import Column, BigInteger, String, Date, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DevUser(Base):
    __tablename__ = 'xz_devUser'
    
    du_nativeID = Column(BigInteger, primary_key=True, comment='用户表主键')
    d_nativeID = Column(BigInteger, comment='设备表主键')
    du_userAccount = Column(String(50))
    du_userName = Column(String(50), comment='用户姓名')
    du_sex = Column(String(1), comment='性别 0:女 1:男')
    du_birthday = Column(Date, comment='生日')
    du_age = Column(Integer, comment='年龄')
    du_mobilPhone = Column(String(20))
    du_userIntro = Column(String(200), comment='用户简介')
    du_chatSummary = Column(String(2048), comment='聊天总结')
    du_voicePrintFilePath = Column(String(100))
    du_createtime = Column(DateTime)
    du_updatetime = Column(DateTime)

class Device(Base):
    __tablename__ = 'xz_device'
    
    d_nativeID = Column(BigInteger, primary_key=True, comment='设备表主键')
    d_devMac = Column(String(50), comment='设备mac')
    d_regStatus = Column(String(1), comment='注册状态 0:未注册，1:已注册')
    d_bindDate = Column(DateTime)
    d_appToken = Column(String(100), comment='APPToken')
    d_protocalVersion = Column(String(10), comment='协议版本')
    d_configJson = Column(Text)

class UserChatMemory(Base):
    __tablename__ = 'xz_userChatMemory'
    
    ucm_nativeID = Column(BigInteger, primary_key=True, comment='聊天记忆表主键')
    du_nativeID = Column(BigInteger, comment='用户表主键')
    ucm_chatDate = Column(Date, comment='聊天日期')
    ucm_chatSummary = Column(String(1000), comment='内容总结')
    ucm_createtime = Column(DateTime)
    ucm_updateTime = Column(DateTime)

class UserSession(Base):
    __tablename__ = 'xz_userSession'
    
    us_nativeid = Column(Integer, primary_key=True)
    du_nativeID = Column(BigInteger, comment='用户表主键')
    us_sessionid = Column(String(50), nullable=False)
    us_bgntime = Column(DateTime)
    us_endtime = Column(DateTime)
    us_content = Column(Text)