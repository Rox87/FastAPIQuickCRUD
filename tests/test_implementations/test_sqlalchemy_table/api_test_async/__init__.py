import asyncio
import os

from fastapi import FastAPI
from sqlalchemy import ARRAY, BigInteger, Boolean, CHAR,Table, Column, Date, DateTime, Float, Integer, \
    JSON, LargeBinary, Numeric, SmallInteger, String, Text, Time, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTERVAL, JSONB, UUID
from sqlalchemy.orm import declarative_base, sessionmaker, synonym


app = FastAPI()

Base = declarative_base()
metadata = Base.metadata

from sqlalchemy import create_engine
TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_ASYNC_URL',
                                   'postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres')

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
engine = create_async_engine(TEST_DATABASE_URL,
                             future=True,
                             echo=True,
                             pool_use_lifo=True,
                             pool_pre_ping=True,
                             pool_recycle=7200)
async_session = sessionmaker(autocommit=False,
                             autoflush=False,
                             bind=engine,
                             class_=AsyncSession)



async def get_transaction_session() -> AsyncSession:
    async with async_session() as session:
        yield session


UntitledTable256 = Table(
    'test_table', metadata,
    Column('primary_key', Integer, primary_key=True, nullable=False,
           server_default=text("nextval('untitled_table_256_id_seq'::regclass)"),info={'alias_name': 'primary_key'}),
    Column('bool_value', Boolean, nullable=False, server_default=text("false")),
    Column('bytea_value', LargeBinary),
    Column('char_value', CHAR(10)),
    Column('date_value', Date, server_default=text("now()")),
    Column('float4_value', Float, nullable=False),
    Column('float8_value', Float(53), nullable=False, server_default=text("10.10")),
    Column('int2_value', SmallInteger, nullable=False),
    Column('int4_value', Integer, nullable=False),
    Column('int8_value', BigInteger, server_default=text("99")),
    Column('interval_value', INTERVAL),
    Column('json_value', JSON),
    Column('jsonb_value', JSONB(astext_type=Text())),
    Column('numeric_value', Numeric),
    Column('text_value', Text),
    Column('time_value', Time),
    Column('timestamp_value', DateTime),
    Column('timestamptz_value', DateTime(True)),
    Column('timetz_value', Time(True)),
    Column('uuid_value', UUID),
    Column('varchar_value', String),
    Column('array_value', ARRAY(Integer())),
    Column('array_str__value', ARRAY(String())),
    UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
)


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_table())