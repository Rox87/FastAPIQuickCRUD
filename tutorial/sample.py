from fastapi import FastAPI
from sqlalchemy import *
from sqlalchemy.orm import *
from fastapi_quickcrud.crud_router import generic_sql_crud_router_builder

Base = declarative_base()

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
DATABASE_URL = "sqlite+aiosqlite:///db/simple_relation.db"
engine = create_async_engine(DATABASE_URL, echo=True)
# engine = create_async_engine('postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres', future=True, echo=True,pool_use_lifo=True, pool_pre_ping=True, pool_recycle=7200)
async_session = sessionmaker(bind=engine, class_=AsyncSession)


async def get_transaction_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session
class Parent(Base):
    __tablename__ = 'parent_o2o'
    id = Column(Integer, primary_key=True, comment='test-test-test')
    name = Column(String, default='ok', unique = True)
    children = relationship("Child", back_populates="parent")



class Child(Base):
    __tablename__ = 'child_o2o'
    id = Column(Integer, primary_key=True, comment='child_pk_test')
    parent_id = Column(Integer, ForeignKey('parent_o2o.id'), info=({'description': 'child_parent_id_test'}), nullable=False)
    parent = relationship("Parent", back_populates="children")


crud_route_parent = generic_sql_crud_router_builder(
    db_model=Parent,
    prefix="/parent",
    tags=["parent"],
)

crud_route_child = generic_sql_crud_router_builder(
    db_model=Child,
    prefix="/child",
    tags=["child"]
)

from fastapi import APIRouter            
router = APIRouter()

@router.on_event("startup")
async def startup_db():
    # Create tables on application startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app = FastAPI()
[app.include_router(i) for i in [router,crud_route_parent, crud_route_child]]
#[app.include_router(i) for i in [crud_route_parent, crud_route_child]]

@app.get("/", tags=["child"])
async def root():
    return {"message": "Hello World"}

import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8002, debug=False)
