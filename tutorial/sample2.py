import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, \
    String, Table, ForeignKey, orm
from fastapi_quickcrud import crud_router_builder

Base = orm.declarative_base()


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
DATABASE_URL = "sqlite+aiosqlite:///./db/friend.db"
engine = create_async_engine(DATABASE_URL, echo=True)
# engine = create_async_engine('postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres', future=True, echo=True,pool_use_lifo=True, pool_pre_ping=True, pool_recycle=7200)
async_session = orm.sessionmaker(bind=engine, class_=AsyncSession)


async def get_transaction_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session

class User(Base):
    __tablename__ = 'test_users'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)


friend = Table(
    'test_friend', Base.metadata,
    Column('id', ForeignKey('test_users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('friend_name', String, nullable=False)
)

crud_route_1 = crud_router_builder(db_model=User,
                                   prefix="/user",
                                   tags=["User"],
                                   async_mode=True
                                   )
crud_route_2 = crud_router_builder(db_model=friend,
                                   prefix="/friend",
                                   tags=["friend"],
                                   async_mode=True
                                   )

app = FastAPI()
from fastapi import APIRouter            
router = APIRouter()

@router.on_event("startup")
async def startup_db():
    # Create tables on application startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
app.include_router(router)        
app.include_router(crud_route_1)
app.include_router(crud_route_2)
uvicorn.run(app, host="0.0.0.0", port=8002)
