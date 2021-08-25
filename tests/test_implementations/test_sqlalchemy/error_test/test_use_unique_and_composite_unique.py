from sqlalchemy import ARRAY, BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, Integer, \
    JSON, LargeBinary, Numeric, SmallInteger, String, Text, Time, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTERVAL, JSONB, UUID
from sqlalchemy.orm import declarative_base, sessionmaker, synonym

from src.fastapi_quickcrud import sqlalchemy_to_pydantic, CrudMethods
from src.fastapi_quickcrud.misc.exceptions import SchemaException

Base = declarative_base()

class UntitledTable256(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key', 'int4_value', 'float4_value']
    __tablename__ = 'test_build_myself_async'
    __table_args__ = (
        UniqueConstraint('id', 'int4_value', 'float4_value'),
    )
    id = Column(Integer, primary_key=True, info={'alias_name': 'primary_key'},autoincrement=True,server_default="nextval('test_build_myself_id_seq'::regclass)")
    primary_key = synonym('id')
    bool_value = Column(Boolean, nullable=False, server_default=text("false"))
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text("now()"))
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text("10.10"))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, server_default=text("99"), unique=True)
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB(astext_type=Text()))
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    uuid_value = Column(UUID(as_uuid=True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))

try:
    UntitledTable256Model = sqlalchemy_to_pydantic(UntitledTable256,
                                                   crud_methods=[
                                                       CrudMethods.UPSERT_MANY,
                                                   ],
                                                   exclude_columns=['bytea_value', 'xml_value', 'box_valaue'])
except SchemaException as e:
    str(e) == 'Only support one unique constraint/ Use unique constraint and composite unique constraint at same time is not supported / Use  composite unique constraint if there are more than one unique constraint'
