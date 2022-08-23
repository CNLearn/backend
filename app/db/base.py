from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base


class BaseWithID:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True, index=True)


# declarative base class
Base = declarative_base(cls=BaseWithID)
