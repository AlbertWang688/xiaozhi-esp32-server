from config.logger import setup_logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status,Depends
from pydantic import BaseModel
#from config.private_config import PrivateConfig  # Assuming this is where your config is stored
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from backend.app.dao.device import DeviceDAO
from backend.app.db import get_session
from backend.app.models.xiaozhi import Device

TAG = __name__
logger = setup_logging()
# Configuration for JWT
SECRET_KEY = "my-secret-key01"  # Replace with a secure secret key
ALGORITHM = "HS256"
# Token expiration time 24 hours
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Default token expiration time


class TokenData(BaseModel):
    dev_mac: Optional[str] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None

#定义OAuth2PasswordBearer依赖（tokenUrl参数指定token的获取地址）
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# oauth2_scheme = HTTPBearer()
security = HTTPBearer()
async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        # expire = datetime.utcnow() + expires_delta
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire,"data":str(data)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def verify_token(token: str) -> TokenData:
async def verify_token(token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify the access token
    :param token: JWT access token
    :return: True if token is valid, False otherwise
    """
    try:
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        dev_dict = payload.get("data")
        dev_mac: str = dev_dict.get("dev_mac")
        expire: datetime = payload.get("exp")
        if dev_mac is None or expire is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if expire < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(**dev_dict)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

async def generate_token_for_device(dev_mac: str,activation_code:str,session=Depends(get_session)) -> str:
    """
    Generate a new access token for the device
    :param dev_mac: Device MAC address
    :return: JWT access token
    """
    # session = get_session()
    device_dao = DeviceDAO(session)
    device = await device_dao.get_by_mac(dev_mac)
    logger.bind(tag=TAG).info(f"device:{device}")
    print(f"device:{device}")
    if not device:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid device :{dev_mac}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #暂时先不验证激活码
    if activation_code and device.d_activationCode != activation_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid activation code for device :{dev_mac}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #将device转换成字典
    dev_dict = {
        "device_id": device.d_nativeID,
        "dev_mac": device.d_devMac,
        # "dev_activationCode": device.d_activationCode,
        "dev_robotNickName": device.d_robotNickName,
        "dev_voiceName": device.d_voiceName,
        "dev_roleIntro": device.d_roleIntro,
        "dev_regStatus": device.d_regStatus,
        "dev_protocalVersion": device.d_protocalVersion
        }
    access_token = create_access_token(data=dev_dict, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_device(token: str = Depends(security)) -> TokenData:
    """
    FastAPI 依赖，统一用于获取并验证当前 token，有效则返回 token 解析后的数据
    """
    return verify_token(token)



