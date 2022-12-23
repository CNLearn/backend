from typing import Optional

from sqlalchemy import JSON, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

word_character_association_table = Table(
    "word_characters",
    Base.metadata,
    Column("word_id", ForeignKey("words.id"), primary_key=True),
    Column("character_id", ForeignKey("characters.id"), primary_key=True),
)


class Character(Base):
    character: Mapped[str] = mapped_column(String(1))
    definition: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    pinyin: Mapped[str] = mapped_column(String(50))
    decomposition: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    etymology: Mapped[Optional[dict[str, str]]] = mapped_column(JSON(), nullable=True)
    radical: Mapped[str] = mapped_column(String(1))
    matches: Mapped[str] = mapped_column(String(300))
    frequency: Mapped[int]
    words: Mapped[set["Word"]] = relationship(secondary=word_character_association_table, back_populates="characters")

    def __repr__(self) -> str:
        return f"<Character({self.character}, radical='{self.radical})>"


class Word(Base):
    simplified: Mapped[str] = mapped_column(String(50))
    traditional: Mapped[str] = mapped_column(String(50))
    pinyin_num: Mapped[str] = mapped_column(String(150))  # at least 104
    pinyin_accent: Mapped[str] = mapped_column(String(100))
    pinyin_clean: Mapped[str] = mapped_column(String(100))
    pinyin_no_spaces: Mapped[str] = mapped_column(String(100))
    also_written: Mapped[str] = mapped_column(String(75))
    also_pronounced: Mapped[str] = mapped_column(String(75))
    classifiers: Mapped[str] = mapped_column(String(25))
    definitions: Mapped[str] = mapped_column(String(500))
    frequency: Mapped[int]
    characters: Mapped[set[Character]] = relationship(
        secondary=word_character_association_table, back_populates="words"
    )

    def __repr__(self) -> str:
        return f"<Word(simplified='{self.simplified}', pinyin='{self.pinyin_accent}'>"
