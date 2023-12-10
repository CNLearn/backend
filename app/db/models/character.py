from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

from .combined import word_character_association_table

if TYPE_CHECKING:
    from .word import Word


class Character(Base):
    # TODO: this one sohuld probably have a unique thing on it
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
