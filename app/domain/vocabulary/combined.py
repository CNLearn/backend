from pydantic import BaseModel, Field

from .character import CharacterSchema
from .word import SimplifiedWord, WordSchema


class WordOut(WordSchema):
    id: int

    characters: list[CharacterSchema] | None = Field(default=[])


class CharacterOut(CharacterSchema):
    id: int

    words: list[WordSchema] | None = Field(default=[])


class DictionarySearchResult(BaseModel):
    words: list[WordSchema]
    not_found: list[SimplifiedWord]
