import httpx
import pytest

# 회원가입 사용자 등록 라우트 테스트
@pytest.mark.asyncio
async def test_sign_new_user(default_client : httpx.AsyncClient) -> None:
    payload = {
        "email" : "a@mail.com",
        "password" : "thebest!"
    }
    headers = {
        "accept" : "application/json",
        "Content-Type" : "application/json"
    }
    test_response = {
        "message" : "User successfully registered"
    }
    response = await default_client.post("/user/signup", json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == test_response

# 로그인 라우트 테스트
@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username" : "a@mail.com", # an email that exists
        "password" : "thebest!"
    }
    headers = {
        "accept" : "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await default_client.post("/user/signin", data=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json()['token_type'] == "Bearer"

