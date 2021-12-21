from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Text, select, insert, delete, update
from typing import Union, Callable, AsyncContextManager, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..crypt import DecryptService, EncryptService
from .base import Base


class User(Base):
    __tablename__ = 'user_data'

    id: Union[Column, int] = Column(Integer, primary_key=True, autoincrement=True)
    created_at: Union[Column, datetime] = Column(DateTime, default=datetime.now)
    updated_at: Union[Column, datetime] = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    username: Union[Column, str] = Column(Text, nullable=False, unique=True)
    password: Union[Column, str] = Column(Text, nullable=False)

    credit_card_number: Union[Column, str] = Column(Text)
    credit_card_pin: Union[Column, str] = Column(Text)
    credit_card_cvv: Union[Column, str] = Column(Text)

    dek: Union[Column, str] = Column(Text)


class UserRepository:
    def __init__(self, session_factory: Callable[..., AsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def insert(
            self,
            username: str,
            password: str,
            credit_card_number: Optional[str] = None,
            credit_card_pin: Optional[str] = None,
            credit_card_cvv: Optional[str] = None,
            dek: Optional[str] = None
    ) -> User:
        async with self.session_factory() as session:
            query = insert(User).values(
                username=username,
                password=password,
                credit_card_number=credit_card_number,
                credit_card_pin=credit_card_pin,
                credit_card_cvv=credit_card_cvv,
                dek=dek
            )
            result = await session.execute(query)
            await session.commit()
            return await self.get(result.inserted_primary_key[0])

    async def update(self, id_: int, **kwargs) -> None:
        async with self.session_factory() as session:
            query = update(User). \
                where(User.id == id_).values(**kwargs)
            await session.execute(query)
            await session.commit()

    async def delete(self, id_: int) -> None:
        async with self.session_factory() as session:
            query = delete(User). \
                where(User.id == id_)
            await session.execute(query)
            await session.commit()

    async def get(self, id_: int) -> Optional[User]:
        async with self.session_factory() as session:
            query = select(User).where(User.id == id_)
            result = await session.execute(query)
            return result.scalar()

    async def get_by_username(self, username: str) -> Optional[User]:
        async with self.session_factory() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            return result.scalar()


class UserService:
    def __init__(
            self,
            session_factory: Callable[..., AsyncContextManager[AsyncSession]],
            encrypt_service: EncryptService,
            decrypt_service: DecryptService,

    ):
        self.repo = UserRepository(session_factory)
        self.encrypt = encrypt_service
        self.decrypt = decrypt_service

    async def insert_with_encrypt(
            self,
            username: str,
            password: str,
            credit_card_number: Optional[int] = None,
            credit_card_pin: Optional[int] = None,
            credit_card_cvv: Optional[int] = None
    ) -> User:
        encrypted_pass = self.encrypt.encrypt_plaintext_password(password)

        if all((credit_card_number, credit_card_pin, credit_card_cvv)):
            dek, chunk = self.encrypt.encrypt_data_chunk([
                str(credit_card_number),
                str(credit_card_pin),
                str(credit_card_cvv)
            ])

            return await self.repo.insert(
                username=username,
                password=encrypted_pass,
                credit_card_number=chunk[0],
                credit_card_pin=chunk[1],
                credit_card_cvv=chunk[2],
                dek=dek
            )
        else:
            return await self.repo.insert(
                username=username,
                password=encrypted_pass,
            )

    async def verify_user_access(self, username: str, password: str) -> bool:
        user = await self.repo.get_by_username(username)
        if not user:
            raise Exception(f'no user by username={username}')
        return self.decrypt.verify_plaintext_with_hash(user.password, password)

    async def get_decrypted_by_username(self, username: str) -> User:
        user = await self.repo.get_by_username(username)
        if not user:
            raise Exception(f'no user by username={username}')

        if all((user.credit_card_number, user.credit_card_pin, user.credit_card_cvv)):

            data_chunk = self.decrypt.decrypt_data_chunk([
                str(user.credit_card_number),
                str(user.credit_card_pin),
                str(user.credit_card_cvv)
            ], user.dek)

            user.credit_card_number = int(data_chunk[0])
            user.credit_card_pin = int(data_chunk[1])
            user.credit_card_cvv = int(data_chunk[2])

            return user
        else:
            return user
