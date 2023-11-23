from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.domain.vocabulary.character import CharacterSchema
from app.domain.vocabulary.common import Character
from app.models.vocabulary import Character as CharacterModel


class CRUDCharacter(CRUDBase[CharacterModel, CharacterSchema, CharacterSchema]):
    async def get_multiple_characters(
        self, db: AsyncSession, *, characters: list[Character], include_words: bool
    ) -> Sequence[CharacterModel]:
        statement = select(CharacterModel).where(CharacterModel.character.in_(characters))
        if include_words:
            statement = statement.options(selectinload(CharacterModel.words))
        result = await db.execute(statement)
        cs = result.scalars().all()
        return cs


character = CRUDCharacter(CharacterModel)
