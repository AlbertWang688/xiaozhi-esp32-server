from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

# 密钥用于签名JWT令牌
SECRET_KEY = "your_secret_key"

app = FastAPI()

security = HTTPBearer()

# 用户数据库模拟
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedpassword",  # 在实际应用中应存储哈希后的密码
    }
}

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

@app.post("/token/")
async def login(username: str, password: str):
    user_dict = fake_users_db.get(username)
    if not user_dict or user_dict["hashed_password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def verify_token(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_dict = fake_users_db.get(username)
    if not user_dict:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**user_dict)

@app.get("/protected-resource/")
async def read_protected_resource(current_user: User = Depends(verify_token)):
    return {"message": f"Hello {current_user.username}"}