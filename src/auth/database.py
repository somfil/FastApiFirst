import uuid
from datetime import datetime, timedelta

from sqlalchemy import select, Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User, Token
from src.settings import settings


class UserDBMethods:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int):
        statement = select(User).where(User.id == user_id)
        return await self._get(statement)

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        return await self._get(statement)

    async def get_token_by_id(self, user_id: int):
        statement = select(Token).where(Token.user_id == user_id)
        return await self._get(statement)

    async def create_new_user(self, data_user: dict):
        user = User(**data_user)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def add_or_update_refresh_token(self, user_id: int):
        existing_token = await self.get_token_by_id(user_id)

        if existing_token is None:
            token = Token(
                user_id=user_id,
                life_time=datetime.utcnow() + timedelta(days=settings.jwt.refresh_token_lifetime)
            )
            self.session.add(token)

        else:
            token = await self._update_token_user(user_id)

        await self.session.commit()
        await self.session.refresh(token)

        return token

    async def _update_token_user(self, user_id: int):
        new_id = str(uuid.uuid4())
        current_time = datetime.utcnow()

        statement = update(Token).where(Token.user_id == user_id).values(
            token=new_id,
            life_time=current_time + timedelta(days=settings.jwt.refresh_token_lifetime)
        ).returning(Token)
        result = await self.session.execute(statement)

        return result.scalar()

    async def _get(self, statement: Select):
        result = await self.session.execute(statement)

        return result.unique().scalar_one_or_none()
