from datetime import datetime, timedelta,timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status,Depends
from pydantic import BaseModel
#from config.private_config import PrivateConfig  # Assuming this is where your config is stored
from fastapi.security import OAuth2PasswordBearer


# Configuration for JWT
SECRET_KEY = "my-secret-key01"  # Replace with a secure secret key
ALGORITHM = "HS256"
# Token expiration time 24 hours
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Default token expiration time

class TokenData(BaseModel):
    dev_mac: Optional[str] = None
#定义OAuth2PasswordBearer依赖（tokenUrl参数指定token的获取地址）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        # expire = datetime.utcnow() + expires_delta
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire,"data":str(data)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """
    Verify the access token
    :param token: JWT access token
    :return: True if token is valid, False otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        dev_mac: str = payload.get("dev_mac")
        if dev_mac is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload missing dev_mac",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(dev_mac=dev_mac)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def generate_token_for_device(dev_mac: str) -> str:
    """
    Generate a new access token for the device
    :param dev_mac: Device MAC address
    :return: JWT access token
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"dev_mac": dev_mac}, expires_delta=access_token_expires)
    return token

def get_current_device(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    FastAPI 依赖，统一用于获取并验证当前 token，有效则返回 token 解析后的数据
    """
    return verify_token(token)
# token1 = generate_token_for_device("00:00:08:00:00:88")
# print("token is:",token1)
# print("jwt.docode is :",jwt.decode(token1, SECRET_KEY, algorithms=[ALGORITHM]))
# print("verify token:",verify_token(token1))
