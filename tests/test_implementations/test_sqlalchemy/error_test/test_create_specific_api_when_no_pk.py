from sqlalchemy import ARRAY, BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, Integer, \
    JSON, LargeBinary, Numeric, SmallInteger, String, Text, Time, text, PrimaryKeyConstraint, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import INTERVAL, JSONB, UUID
from sqlalchemy.orm import declarative_base, synonym

from src.fastapi_quickcrud.misc.utils import table_to_declarative_base
from src.fastapi_quickcrud import sqlalchemy_to_pydantic, CrudMethods
from src.fastapi_quickcrud.misc.exceptions import SchemaException, ColumnTypeNotSupportedException, PrimaryMissing

Base = declarative_base()

metadata = Base.metadata
UntitledTable256 = Table(
    'test_table', metadata,
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
UniqueConstraint('interval_value', 'numeric_value', 'text_value'),
)

UntitledTable256 = table_to_declarative_base(UntitledTable256)
try:

    UntitledTable256Model = sqlalchemy_to_pydantic(UntitledTable256,
                                                   crud_methods=[
                                                       CrudMethods.PATCH_ONE,
                                                   ],
                                                   exclude_columns=['xml_value', 'box_valaue','__id'])
except PrimaryMissing as e:
    assert 'The generation of this API [PATCH_ONE] requires a primary key' in str(e)


try:
    UntitledTable256Model = sqlalchemy_to_pydantic(UntitledTable256,
                                                   crud_methods=[
                                                       CrudMethods.FIND_ONE,
                                                   ],
                                                   exclude_columns=['xml_value', 'box_valaue','__id'])
except PrimaryMissing as e:
    print(str(e))
    assert 'The generation of this API [FIND_ONE] requires a primary key' in str(e)


try:
    UntitledTable256Model = sqlalchemy_to_pydantic(UntitledTable256,
                                                   crud_methods=[
                                                       CrudMethods.DELETE_ONE,
                                                   ],
                                                   exclude_columns=['xml_value', 'box_valaue','__id'])
except PrimaryMissing as e:
    print(str(e))
    assert 'The generation of this API [DELETE_ONE] requires a primary key' in str(e)


try:
    UntitledTable256Model = sqlalchemy_to_pydantic(UntitledTable256,
                                                   crud_methods=[
                                                       CrudMethods.UPDATE_ONE,
                                                   ],
                                                   exclude_columns=['xml_value', 'box_valaue','__id'])
except PrimaryMissing as e:
    print(str(e))
    assert 'The generation of this API [UPDATE_ONE] requires a primary key' in str(e)


try:
    UntitledTable256Model = sqlalchemy_to_pydantic(UntitledTable256,
                                                   crud_methods=[
                                                       CrudMethods.POST_REDIRECT_GET,
                                                   ],
                                                   exclude_columns=['xml_value', 'box_valaue','__id'])
except PrimaryMissing as e:
    print(str(e))
    assert 'The generation of this API [POST_REDIRECT_GET] requires a primary key' in str(e)

