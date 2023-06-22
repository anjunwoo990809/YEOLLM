from pydantic import BaseModel
# from sqlmodel import JSON, SQLModel, Field, Column
from beanie import Document
from typing import List, Optional

# 몽고 DB를 사용하도록 설정
class Event(Document):
    creator : Optional[str]
    
    original_content : str
    story_summary : str
    scenario : str
    
    class Config:
        schema_extra = {
            "example" : {
                "original_content" : "Book",
                "story_summary" : "Once upon a time, there was a dinosaur.",
                "scenario" : "A : What's that? \n B : That's a ... dinosaur...!"
            }
        }

    class Settings:
        name = "events"

class EventUpdate(BaseModel):
    original_content : Optional[str]
    story_summary : Optional[str]
    scenario : Optional[str]
    
    class Config:
        schema_extra={
            "example" : {
                "story_summary" : "Once upon a time, there was a creature.",
                "scenario" : "A : What's that? \n B : That's a ... creature...!"
            }
        }


# class Event(SQLModel, table=True):
#     id : int = Field(default=None, primary_key=True)
#     title : str
#     image : str
#     description : str
#     tags : List[str] = Field(sa_column=Column(JSON))
#     location : str
    
#     # event의 sample data를 정의 (API를 통해 신규 이벤트 생성 시 참고 가능)
#     class Config:
#         arbitrary_types_allowed = True
#         schema_extra = {
#             "example" : {
#                 "title": "FastAPI Book Launch",
#                 "image": "image_path",
#                 "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
#                 "tags": ["python", "fastapi", "book", "launch"],
#                 "location": "Google Meet"
#             }
#         }

# class EventUpdate(SQLModel):
#     title : Optional[str]
#     image : Optional[str]
#     description : Optional[str]
#     tags : Optional[str]
#     location : Optional[str]
    
#     class Config:
#         schema_extra={
#             "example" : {
#                 "title": "FastAPI Book Launch",
#                 "image" : "https~",
#                 "description" : "We will discuss later",
#                 "tags" : ["python", "fastapi", "book", "launch"],
#                 "location" : "Google Meet"
#             }
#         }
