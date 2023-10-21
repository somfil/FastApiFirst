import datetime

from src import exceptions
from src.auth import models
from src.auth.database import UserDBMethods
from src.auth.jwt_token import JWTSecurity
from src.auth.schemas import UserRegistrationSchema, AuthUserCustomForm
from src.auth.security import PasswordHelper


class ServiceUserManager:
    db_connect: UserDBMethods

    def __init__(self, db_connect: UserDBMethods):
        self.db_connect = db_connect
        self.password_helper = PasswordHelper()
        self.jwt_security = JWTSecurity()

    async def get_user_by_id(self, user_id: int) -> models.UP:
        user_id = await self.db_connect.get_user_by_id(user_id)

        if user_id is None:
            raise exceptions.UserNotExist

        return user_id

    async def get_user_by_email(self, email: str) -> models.UP:
        email_user = await self.db_connect.get_user_by_email(email)

        if email_user is None:
            raise exceptions.UserNotExist

        return email_user

    async def get_token_by_id(self, user_id: int) -> models.TP:
        token = await self.db_connect.get_token_by_id(user_id)

        if token is None:
            raise exceptions.TokenNotExist

        return token

    async def check_validity_token_in_database(self, user_id: int, token_cookie: str):
        existing_token = await self.get_token_by_id(user_id)

        current_time = datetime.datetime.utcnow()

        if current_time > existing_token.life_time:
            raise exceptions.InvalidExistingToken()

        elif existing_token.token != token_cookie:
            raise exceptions.InvalidExistingToken()

        return await self.db_connect.add_or_update_refresh_token(user_id)

    async def check_user_token(self, user_id: int) -> models.TP:
        return await self.db_connect.add_or_update_refresh_token(user_id)

    async def create(self, data_user: UserRegistrationSchema) -> models.UP:
        existing_user = await self.db_connect.get_user_by_email(data_user.email)

        if existing_user is not None:
            raise exceptions.UserAlreadyExist

        user_dict = data_user.model_dump()
        password = user_dict.pop('password')
        user_dict['hashed_password'] = self.password_helper.hash(password)

        create_new_user = await self.db_connect.create_new_user(user_dict)
        return create_new_user

    async def authentication(self, credentials: AuthUserCustomForm):
        try:
            user = await self.get_user_by_email(credentials.email)

        except exceptions.UserNotExist:
            self.password_helper.hash(credentials.password)
            raise exceptions.UserNotExist

        verified = self.password_helper.verify_password(
            credentials.password, user.hashed_password
        )
        if not verified:
            raise exceptions.InvalidCredentials

        return user

    async def create_access_token(self, user_id: int):
        access_token = await self.jwt_security.create_token(user_id)
        return access_token
