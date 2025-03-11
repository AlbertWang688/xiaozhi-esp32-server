from sqlmodel import Session, select
from typing import List, Optional
from backend.app.models.xiaozhi import Device
from datetime import datetime

class DeviceDAO:
    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def entity_format(cls, device):
        """
        将设备对象中的时间字段从字符串转换为datetime对象。       
        :param device: 设备对象
        """
        if device.d_createTime and isinstance(device.d_createTime, str):
            device.d_createTime = datetime.fromisoformat(device.d_createTime)
        if device.d_registerTime and isinstance(device.d_registerTime, str):
            device.d_registerTime = datetime.fromisoformat(device.d_registerTime)
        if device.d_updateTime and isinstance(device.d_updateTime, str):
            device.d_updateTime = datetime.fromisoformat(device.d_updateTime)

    async def create(self, device: Device) -> Device:
        self.entity_format(device)
        self.session.add(device)
        self.session.commit()
        self.session.refresh(device)
        return device

    async def get_by_id(self, device_id: int) -> Optional[Device]:
        return self.session.get(Device, device_id)

    async def get_by_mac(self, mac: str) -> Optional[Device]:
        statement = select(Device).where(Device.d_devMac == mac)
        return self.session.exec(statement).first()

    async def update(self, device_id: int, device: Device) -> Optional[Device]:
        db_device = await self.get_by_id(device_id)
        if not db_device:
            return None
        
        device_data = device.model_dump(exclude_unset=True)
        for key, value in device_data.items():
            setattr(db_device, key, value)
        
        self.session.add(db_device)
        self.session.commit()
        self.session.refresh(db_device)
        return db_device

    async def delete(self, device_id: int) -> bool:
        device = await self.get_by_id(device_id)
        if not device:
            return False
        self.session.delete(device)
        self.session.commit()
        return True
