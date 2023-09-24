from pydantic import Field

from .character import CharacterSchema
from .word import WordSchema


class WordOut(WordSchema):
    id: int

    characters: list[CharacterSchema] | None = Field(default=[])


class CharacterOut(CharacterSchema):
    id: int

    words: list[WordSchema] | None = Field(default=[])
