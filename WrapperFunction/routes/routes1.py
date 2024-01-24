from WrapperFunction.src.fastapi_quickcrud.crud_router import generic_sql_crud_router_builder
from WrapperFunction.models.model1 import Child, Parent
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