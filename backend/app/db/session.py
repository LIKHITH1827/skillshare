from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Async engine for SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create async session factory
async_session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency for FastAPI
async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
