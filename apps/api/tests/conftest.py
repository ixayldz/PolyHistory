import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import get_settings

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/test_polyhistory"
DB_AVAILABLE = False

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    future=True,
    echo=False
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def override_get_db():
    """Override database dependency for testing."""
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Set up test database."""
    global DB_AVAILABLE

    async def _setup():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def _teardown():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    try:
        asyncio.run(_setup())
        DB_AVAILABLE = True
    except Exception:
        DB_AVAILABLE = False

    yield

    if DB_AVAILABLE:
        asyncio.run(_teardown())


@pytest_asyncio.fixture
async def db_session():
    """Get test database session."""
    if not DB_AVAILABLE:
        pytest.skip("Test database is not available on localhost:5433")
    async with TestSessionLocal() as session:
        yield session
        # Clean up after test
        await session.rollback()


@pytest_asyncio.fixture
async def client():
    """Get test HTTP client."""
    if not DB_AVAILABLE:
        pytest.skip("Test database is not available on localhost:5433")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def test_user(client):
    """Create a test user and return user data with tokens."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    # Register user
    response = await client.post("/api/v1/auth/register", json=user_data)
    if response.status_code == 201:
        user = response.json()
    else:
        # User might already exist, try to login
        login_response = await client.post("/api/v1/auth/login", json=user_data)
        user = login_response.json()
        return user_data, user
    
    # Login to get tokens
    login_response = await client.post("/api/v1/auth/login", json=user_data)
    tokens = login_response.json()
    
    return user_data, tokens


@pytest.fixture
def auth_headers(test_user):
    """Get authorization headers for authenticated requests."""
    _, tokens = test_user
    return {"Authorization": f"Bearer {tokens['access_token']}"}
