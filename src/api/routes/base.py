from fastapi_crudrouter import SQLAlchemyCRUDRouter

from src.api.schemas.users import User, UserCreate
from src.database.models import UserModel
from src.database.sql import get_db


def add_route(schema, create_schema, db_model, prefix, create_route=False):
    route = SQLAlchemyCRUDRouter(
        schema=schema,
        create_schema=create_schema,
        db_model=db_model,
        db=get_db,
        prefix=prefix,
        create_route=create_route,
        # dependencies=[Depends(AuthHandler().auth_wrapper)]
    )
    return route


users = add_route(User, UserCreate, UserModel, 'users')
