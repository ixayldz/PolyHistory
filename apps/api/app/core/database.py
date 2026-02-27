from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
import logging

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()

POLYHISTORY_TABLES = [
    "claim_evidence",
    "audit_logs",
    "model_outputs",
    "claims",
    "snippets",
    "evidence_items",
    "cases",
    "users",
]


async def get_db():
    """Dependency for getting database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        # Ensure model metadata is registered before create_all.
        import app.models  # noqa: F401

        try:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        except Exception as exc:
            # Some managed Postgres environments do not permit extension creation.
            logger.warning("Could not ensure pgvector extension on startup: %s", exc)

        result = await conn.execute(
            text(
                """
                SELECT udt_name
                FROM information_schema.columns
                WHERE table_schema = current_schema()
                  AND table_name = 'users'
                  AND column_name = 'id'
                """
            )
        )
        row = result.first()

        if row and row[0] != "uuid":
            logger.warning(
                "Detected incompatible users.id type (%s). Resetting PolyHistory tables.",
                row[0],
            )
            for table in POLYHISTORY_TABLES:
                await conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))

        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections."""
    await engine.dispose()
