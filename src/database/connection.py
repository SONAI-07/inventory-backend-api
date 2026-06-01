from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os

#Equivalent of a global configuration for all @Entity classes

Base = declarative_base()


# We will load this from the .env file later, but here is a default fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/inventory_db")

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Dependency to inject DB sessions into routers
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()