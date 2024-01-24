from fastapi import FastAPI
from fastapi import APIRouter
from sqlalchemy import orm
from WrapperFunction.routes.routes1 import crud_route_parent, crud_route_child
from WrapperFunction.db.database import engine
router = APIRouter()
Base = orm.declarative_base()
@router.on_event("startup")
async def startup_db():
    # Create tables on application startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app = FastAPI()
[app.include_router(i) for i in [router,crud_route_parent, crud_route_child]]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, debug=False)
