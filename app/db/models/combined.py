from sqlalchemy import Column, ForeignKey, Table

from app.db.models.base import Base

word_character_association_table = Table(
    "word_characters",
    Base.metadata,
    Column[int]("word_id", ForeignKey("words.id"), primary_key=True),
    Column[int]("character_id", ForeignKey("characters.id"), primary_key=True),
)
