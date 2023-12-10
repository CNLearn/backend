from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain.vocabulary.combined import CharacterOut, WordOut

from .dependencies import search as search_dependencies

router = APIRouter()


@router.get("/get-words", response_model=list[WordOut], name="vocabulary:get-words")
async def get_words(
    result: Annotated[list[WordOut], Depends(search_dependencies.search_simplified_words)]
) -> list[WordOut]:
    return result


@router.get("/get-characters", response_model=list[CharacterOut], name="vocabulary:get-characters")
async def get_characters(
    result: Annotated[list[CharacterOut], Depends(search_dependencies.search_characters)]
) -> list[CharacterOut]:
    return result
