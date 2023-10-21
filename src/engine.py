from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.settings import settings


engine = create_async_engine(settings.db_url.url, echo=False, future=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=True)

Base = declarative_base()


async def get_async_session():
    async with async_session() as session:
        yield session
