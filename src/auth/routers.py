from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, RedirectResponse

from src import exceptions
from src.auth import models
from src.auth.dependencies import get_custom_servers, get_current_user
from src.auth.schemas import UserResponseSchema, UserRegistrationSchema, TokenResponseSchema, AuthUserCustomForm
from src.auth.manager import ServiceUserManager


router = APIRouter()


@router.post(
    '/sign-in',
    response_model=UserResponseSchema
)
async def register_new_user(
        data_user: UserRegistrationSchema,
        service: ServiceUserManager = Depends(get_custom_servers)
):
    try:
        add_new_user = await service.create(data_user)

    except exceptions.UserAlreadyExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='REGISTER_USER_ALREADY_EXISTS'
        )
    return add_new_user


@router.post(
    '/log-in',
    response_model=TokenResponseSchema,
    status_code=201
)
async def login_user(
        response: Response,
        credentials: Annotated[AuthUserCustomForm, Depends()],
        service: ServiceUserManager = Depends(get_custom_servers)
):
    try:
        existing_user = await service.authentication(credentials)

    except exceptions.UserNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='LOGIN_BAD_CREDENTIALS'
        )

    except exceptions.InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='LOGIN_USER_NOT_VERIFIED'
        )

    user_token = await service.check_user_token(existing_user.id)

    user_access_token = await service.create_access_token(user_token.user_id)

    response.set_cookie(
        'tokenSession',
        user_token.token,
        secure=True,
        httponly=True
    )
    return {'access_token': user_access_token, 'token_type': 'bearer'}


@router.post(
    '/refresh-token',
    response_model=TokenResponseSchema)
async def refresh_token(
        request: Request,
        response: Response,
        user: models.UP = Depends(get_current_user),
        service: ServiceUserManager = Depends(get_custom_servers)
):
    cookie = request.cookies.get('tokenSession')
    try:
        valid_token = await service.check_validity_token_in_database(user.id, cookie)

    except exceptions.InvalidExistingToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='INVALID TOKEN'
        )

    user_access_token = await service.create_access_token(valid_token.user_id)

    response.set_cookie(
        'tokenSession',
        valid_token.token,
        secure=True,
        httponly=True
    )
    return {'access_token': user_access_token, 'token_type': 'bearer'}