from typing import NewType

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import TypedDict

from .common import Character, Definition, Frequency, PinyinToneMarks

Decomposition = NewType("Decomposition", str)
Radical = NewType("Radical", str)
Matches = NewType("Matches", str)


class Etymology(TypedDict, total=False):
    semantic: str
    phonetic: str
    hint: str
    type: str


class CharacterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    character: Character = Field(min_length=1, max_length=1)
    definition: Definition | None
    pinyin: PinyinToneMarks = Field(min_length=0, max_length=50)
    decomposition: Decomposition | None
    etymology: Etymology | None
    radical: Radical = Field(min_length=1, max_length=1)
    matches: Matches = Field(min_length=0, max_length=300)
    frequency: Frequency = Field(gt=0)
