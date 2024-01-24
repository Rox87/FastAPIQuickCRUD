from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite+aiosqlite:///db/simple_relation.db"
engine = create_async_engine(DATABASE_URL, echo=True)
# engine = create_async_engine('postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres', future=True, echo=True,pool_use_lifo=True, pool_pre_ping=True, pool_recycle=7200)
async_session = sessionmaker(bind=engine, class_=AsyncSession)


async def get_transaction_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session