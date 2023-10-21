import uuid
from datetime import datetime
from typing import Protocol, TypeVar

from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.engine import Base


class UserProtocol(Protocol):
    id: int
    email: str
    hashed_password: str


class TokenProtocol(Protocol):
    id: int
    token: str
    life_time: datetime
    user_id: int


UP = TypeVar('UP', bound=UserProtocol)
TP = TypeVar('TP', bound=TokenProtocol)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    tokens = relationship('Token', back_populates='user')


class Token(Base):
    __tablename__ = 'tokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    token: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    life_time: Mapped[datetime] = mapped_column(TIMESTAMP, default=None)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tokens')


