import asyncio # 활성 루프 세션을 만들어 테스트가 단일 스레드로 실행되게 함
import httpx # HTTP CRUD 처리를 위한 비동기 클라이언트 역할
import pytest # 픽스처 정의를 위해 사용

from main import app # Application Instance
from database.connection import Settings
from models.events import Event
from models.users import User

# loop session fixture
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

# new DB instance
async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

    await test_settings.initialize_database()

# basic client fixture
@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
        # 리소스 정리
        await Event.find_all().delete()
        await User.find_all().delete()