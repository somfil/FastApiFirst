
from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from src import exceptions
from src.auth.database import UserDBMethods
from src.auth.manager import ServiceUserManager
from src.engine import get_async_session


token_key = APIKeyHeader(name='Authorization')


async def get_database(session: AsyncSession = Depends(get_async_session)):
    yield UserDBMethods(session)


async def get_custom_servers(db_connect=Depends(get_database)):
    yield ServiceUserManager(db_connect)


async def get_current_user(
        token: Annotated[str, Depends(token_key)],
        service: ServiceUserManager = Depends(get_custom_servers)
):
    user_not_unauthorized = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='UNAUTHORIZED'
        )
    try:
        user_id = await service.jwt_security.read_token(token)

    except exceptions.InvalidExistingToken:
        raise user_not_unauthorized

    except exceptions.PyJWTError:
        raise user_not_unauthorized

    try:
        get_user = await service.get_user_by_id(user_id)

    except exceptions.UserNotExist:
        raise user_not_unauthorized

    return get_user
