from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.vocabulary import character as character_domain
from app.domain.vocabulary import common as common_vocabulary_domain

from ..models import character as character_model
from .base import CRUDBase


class CRUDCharacter(
    # TODO: the update should probably be rethought of
    # probably nothing to be updated
    CRUDBase[character_model.Character, character_domain.CharacterSchema, character_domain.CharacterSchema]
):
    async def get_multiple_characters(
        self, db: AsyncSession, *, characters: list[common_vocabulary_domain.Character], include_words: bool
    ) -> Sequence[character_model.Character]:
        statement = select(character_model.Character).where(character_model.Character.character.in_(characters))
        if include_words:
            statement = statement.options(selectinload(character_model.Character.words))
        result = await db.execute(statement)
        cs = result.scalars().all()
        return cs


character_crud = CRUDCharacter(character_model.Character)
