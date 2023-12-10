from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from app.db.models import character as character_model
from app.db.models import word as word_model
from app.settings.db import db_settings
from tests.fixtures.data import sample_characters, sample_words


def add_some_words_and_characters() -> None:
    postgres_uri = str(db_settings.CNLEARN_POSTGRES_URI)
    postgres_uri = postgres_uri.replace("+asyncpg", "+psycopg")
    engine = create_engine(postgres_uri)
    engine.connect()
    Session = sessionmaker(engine)
    with Session() as session:
        characters_to_add = sample_characters()
        words_to_add = sample_words()
        for character_schema in characters_to_add:
            character_obj = character_model.Character(**character_schema.model_dump())
            session.add(character_obj)
        for word_schema in words_to_add:
            word_obj = word_model.Word(**word_schema.model_dump())
            session.add(word_obj)
        session.commit()
        all_words = session.execute(select(word_model.Word)).scalars()
        for word in all_words:
            characters: set[str] = set(character for character in word.simplified if character.isalpha())
            if not characters:
                continue
            else:
                # let's get the character object
                character_set: set[character_model.Character] = set()
                for character in characters:
                    try:
                        character_object = session.execute(
                            select(character_model.Character).where(character_model.Character.character == character)
                        ).scalar_one()
                    except NoResultFound:
                        pass
                    else:
                        character_set.add(character_object)
                if character_set:
                    word.characters = character_set
                    session.add(word)
        session.commit()
    engine.dispose()
    # add a sleep here
