import asyncio
from typing import AsyncGenerator, Generator
import pytest
import httpx
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.session import Base, get_db
from app.main import app

# InMemory SQLite database for testing purposes
DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

# Create async engine for SQLite
test_engine = create_async_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
)

# Async session factory for tests
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def initialize_test_db():
    """Create database tables in memory and clean them up after the session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture(autouse=True)
async def clean_database():
    """Clean up and truncate all tables before each test execution to ensure isolation."""
    # Truncate tables for SQLite by deleting all items
    async with TestSessionLocal() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
    yield


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an isolated testing database session."""
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """FastAPI AsyncClient fixture overriding get_db to inject the test database session."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
