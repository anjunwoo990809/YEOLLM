from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event
from beanie import Document, Link

# 사용자 개인 info
# class User(BaseModel): # without MongoDB
class User(Document):
    email : EmailStr
    password : str
    events : Optional[List[Event]] # 해당 사용자가 생성한 이벤트, 처음에는 비어 있음
    
    class Settings:
        name = "users"
    
    # example
    class Config:
        schema_extra = {
            "example" : {
                "email" : "somebody@gmail.com",
                "username" : "junwooAhn",
                "events" : [],
            }
        }

# UserSignIn -> TokenResponse
class TokenResponse(BaseModel):
    access_token : str
    token_type : str
