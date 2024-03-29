from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker: async_sessionmaker[AsyncSession] = request.state._db
    async with async_session_maker() as async_session:
        yield async_session
