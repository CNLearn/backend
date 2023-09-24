from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.domain.vocabulary.character import CharacterSchema
from app.domain.vocabulary.common import Character
from app.models.vocabulary import Character as CharacterModel


class CRUDCharacter(CRUDBase[CharacterModel, CharacterSchema, CharacterSchema]):
    async def get_by_character(
        self, db: AsyncSession, *, character: Character, include_words: bool
    ) -> CharacterModel | None:
        statement = select(CharacterModel).where(CharacterModel.character == character)
        if include_words:
            statement = statement.options(selectinload(CharacterModel.words))
        result = await db.execute(statement)
        c = result.scalar_one_or_none()
        return c


character = CRUDCharacter(CharacterModel)
