from sqlalchemy import Column, Integer, ForeignKey,String, orm

Base = orm.declarative_base()
metadata = Base.metadata
class Child(Base):
    __tablename__ = 'child_o2o'
    id = Column(Integer, primary_key=True, comment='child_pk_test')
    parent_id = Column(Integer, ForeignKey('parent_o2o.id'), info=({'description': 'child_parent_id_test'}), nullable=False)
    parent = orm.relationship("Parent", back_populates="children")
    
class Parent(Base):
    __tablename__ = 'parent_o2o'
    id = Column(Integer, primary_key=True, comment='test-test-test')
    name = Column(String, default='ok', unique = True)
    children = orm.relationship("Child", back_populates="parent")