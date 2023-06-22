# test for CRUD
import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event

# 개인화된 아이템을 관리하기 위해 접속 토큰 생성하는 픽스처, 모듈 단위의 범위
@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("a@mail.com")

# 이벤트를 DB에 추가하는 픽스처, CRUD 라우트 테스트에 대한 사전 테스트를 진행하는데 사용됨.
@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event = Event(
        creator="a@mail.com",
        original_content="Book",
        story_summary="Once upon a time, there was a dinosaur.",
        scenario="A : What's that? \n B : That's a ... dinosaur...!",
    )
    await Event.insert_one(new_event)
    
    yield new_event

# /event (prefix) route의 GET method Test : OK
@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")
    
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)

# /event/{id} route GET method Test
@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)
    
    assert response.status_code == 200
    assert response.json()['creator'] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)

# 생성 라우트
@pytest.mark.asyncio
async def test_post_event(default_client : httpx.AsyncClient, access_token : str) -> None:
    payload = {
        "original_content" : "Book",
        "story_summary" : "Once upon a time, there was a dinosaur.",
        "scenario" : "A : What's that? \n B : That's a ... dinosaur...!"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {
        "message": "Event created successfully"
    }
    response = await default_client.post("/event/new", json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == test_response

@pytest.mark.asyncio
async def test_get_events_count(default_client : httpx.AsyncClient) -> None:
    response = await default_client.get("/event/")
    
    events = response.json()
    
    assert response.status_code == 200
    assert len(events) == 2

# 변경 라우트
@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: Event, access_token : str) -> None:
    test_payload = {
        "story_summary" : "It was not a dinosaur. It was unknown creature.",
        "scenario" : "A : What's that? \n B : That's a ... I don't know...!"
    }
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}"
    }
    url = f"/event/{str(mock_event.id)}"
    
    response = await default_client.put(url, json=test_payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["story_summary"] == test_payload["story_summary"]
    assert response.json()["scenario"] == test_payload["scenario"]

# 삭제 라우트
@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event : Event, access_token : str) -> None:
    test_response = {
        "message" : "Event deleted successfully."
    }
    
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}"
    }
    
    url = f"/event/{mock_event.id}"
    
    response = await default_client.delete(url, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == test_response

# 삭제 확인 테스트
@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient, mock_event : Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)
    
    assert response.status_code == 404
