from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.domain.vocabulary.word import SimplifiedWord, WordSchema
from app.models.vocabulary import Word as WordModel


class CRUDWord(CRUDBase[WordModel, WordSchema, WordSchema]):
    async def get_multiple_simplified(
        self, db: AsyncSession, *, simplified_words: list[SimplifiedWord]
    ) -> Sequence[WordModel]:
        statement = (
            select(WordModel)
            .where(WordModel.simplified.in_(simplified_words))
            .options(selectinload(WordModel.characters))
        )
        result = await db.execute(statement)
        return result.scalars().all()


word = CRUDWord(WordModel)
