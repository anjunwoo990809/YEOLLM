from fastapi import APIRouter, Depends, HTTPException, Request, status
# Depends : 의존성 주입을 담당, 함수를 인수로 사용하거나 함수 인수를 라우트에 전달할 수 있게 함.
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List

# mongoDB
from beanie import PydanticObjectId
from database.connection import Database

from auth.authenticate import authenticate


event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)

# 모든 이벤트를 추출하거나 특정 ID의 이벤트만 추출하는 라우트 정의
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retieve_event(id : PydanticObjectId) -> Event:
    # event = session.get(Event, id)
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event


# 이벤트 생성
# DB처리에 필요한 세션 객체가 get_session() 함수에 의존하도록 설정함
@event_router.post("/new")
async def create_event(body : Event, user : str = Depends(authenticate)) -> dict :
    # 개인 영역에서만 업로드 가능
    body.creator = user
    await event_database.save(body)
    return {
        "message": "Event created successfully"
    }

# 이벤트 변경
@event_router.put("/{id}", response_model=Event)
async def update_event(id : PydanticObjectId, body : EventUpdate, user : str = Depends(authenticate)) -> Event :
    """
    라우트 함수에 특정 이벤트를 추출해서 변경하는 코드 작성
    """
    # 수정 권한 확인
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    # 업데이트 진행
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

# 삭제
@event_router.delete("/{id}")
async def delete_event(id : PydanticObjectId, user : str = Depends(authenticate)) -> dict:
    
    event_by_id = await event_database.get(id)
    if event_by_id.creator != user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not allowed"
        )
    
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return {
        "message" : "Event deleted successfully."
    }