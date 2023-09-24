from typing import NewType

from pydantic import BaseModel, ConfigDict, Field

from .common import (
    Definition,
    Frequency,
    PinyinNoSpacesNoToneMarks,
    PinyinNoToneMarks,
    PinyinToneMarks,
    PinyinToneNumbers,
)

Word = NewType("Word", str)
SimplifiedWord = NewType("SimplifiedWord", Word)
TraditionalWord = NewType("TraditionalWord", Word)
AlsoWritten = NewType("AlsoWritten", str)
AlsoPronounced = NewType("AlsoPronounced", str)
Classifiers = NewType("Classifiers", str)


class WordSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    simplified: SimplifiedWord = Field(min_length=1, max_length=50)
    traditional: TraditionalWord = Field(min_length=1, max_length=50)
    pinyin_num: PinyinToneNumbers = Field(min_length=1, max_length=150)
    pinyin_accent: PinyinToneMarks = Field(min_length=1, max_length=100)
    pinyin_clean: PinyinNoToneMarks = Field(min_length=1, max_length=100)
    pinyin_no_spaces: PinyinNoSpacesNoToneMarks = Field(min_length=1, max_length=100)
    also_written: AlsoWritten = Field(min_length=0, max_length=75)
    also_pronounced: AlsoPronounced = Field(min_length=0, max_length=75)
    classifiers: Classifiers = Field(min_length=0, max_length=25)
    definitions: Definition = Field(min_length=0, max_length=500)
    frequency: Frequency = Field(gt=0)
