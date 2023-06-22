import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError # for encoding and decoding
from database.connection import Settings

# SECRET_KEY 변수 추출을 위해 Settings 클래스 인스턴스 생성
settings = Settings()

def create_access_token(user : str):
    payload = {
        "user" : user,
        "expires" : time.time() + 3600
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def verify_access_token(token : str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")
        
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Access Token Supplied.",
            )
            
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail = "Token expired!"
            )
        
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Token"
        )
