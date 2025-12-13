import ssl
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

# ✅ Ensure models are imported for metadata creation
# from app.models import *  # uncomment and import your models here

# Path to your SSL certificate (use raw string or escape properly)
ssl_cert_path = "certificates/ca.pem"
# Database URL
DATABASE_URL = (
    "postgresql+asyncpg://neondb_owner:npg_SCz1mvyf0bqp@"
    "ep-cool-poetry-a14jd07k-pooler.ap-southeast-1.aws.neon.tech/"
    "neondb"
    # "?sslmode=require"
)




# ✅ Create SSL context
# ssl_context = ssl.create_default_context(cafile=ssl_cert_path)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=1,
    max_overflow=0,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ✅ Base class for models
Base = declarative_base()


# ✅ Dependency for FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


# ✅ Function to auto-create tables
async def init_models():
    """Create all database tables asynchronously."""
    async with engine.begin() as conn:
        # Optional: test connection
        # await conn.execute(text("SELECT 1"))
        # Automatically create all tables
        await conn.run_sync(Base.metadata.create_all)


