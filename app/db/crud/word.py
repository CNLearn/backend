from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.vocabulary import word as word_domain

from ..models import word as word_model
from .base import CRUDBase


class CRUDWord(CRUDBase[word_model.Word, word_domain.WordSchema, word_domain.WordSchema]):
    async def get_multiple_simplified(
        self, db: AsyncSession, *, simplified_words: list[word_domain.SimplifiedWord]
    ) -> Sequence[word_model.Word]:
        statement = (
            select(word_model.Word)
            .where(word_model.Word.simplified.in_(simplified_words))
            .options(selectinload(word_model.Word.characters))
        )
        result = await db.execute(statement)
        return result.scalars().all()


word_crud = CRUDWord(word_model.Word)
