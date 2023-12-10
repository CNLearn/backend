from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

from .combined import word_character_association_table

if TYPE_CHECKING:
    from .character import Character


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
    characters: Mapped[set["Character"]] = relationship(
        secondary=word_character_association_table, back_populates="words"
    )

    def __repr__(self) -> str:
        return f"<Word(simplified='{self.simplified}', pinyin='{self.pinyin_accent})'>"
