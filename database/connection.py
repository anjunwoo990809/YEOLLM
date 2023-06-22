from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic import BaseSettings, BaseModel

from models.users import User
from models.events import Event

class Settings(BaseSettings):
    SECRET_KEY: Optional[str] = None
    
    DATABASE_URL : Optional[str] = None
    
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                        document_models=[Event, User])
    
    class Config:
        env_file = ".env"


database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}" # 없는 경우 생성
connect_args = {"check_same_thread":False}
engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)


def conn():
    """
    SQLModel을 사용해 데이터베이스와 테이블을 생성한다.
    """
    SQLModel.metadata.create_all(engine_url)

def get_session():
    """
    데이터베이스 세션을 애플리케이션 내에서 유지한다.
    """
    with Session(engine_url) as session:
        yield session

class Database:
    """
    초기화 시 모델을 인수로 받음, 초기화 중 사용되는 모델은 Event 또는 User 문서의 모델
    """
    def __init__(self, model) -> None:
        self.model = model
    
    # Create
    async def save(self, document) -> None:
        """
        Adding a single record to the DB collection.
        문서의 인수를 받아 DB 인스턴스에 전달함.
        """
        await document.create()
        return
    
    # Read
    async def get(self, id : PydanticObjectId) -> Any :
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    async def get_all(self) -> List[Any] :
        docs = await self.model.find_all().to_list()
        return docs
    
    # Update
    async def update(self, id:PydanticObjectId, body : BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()
        des_body = {k:v for k,v in des_body.items() if v is not None}
        update_query = {"$set" : {
            field : value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc                                                                                        
    
    # Delete
    async def delete(self, id : PydanticObjectId) -> bool :
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True