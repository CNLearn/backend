from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from app.api.dependencies import search
from app.domain.vocabulary.combined import CharacterOut, WordOut

router = APIRouter()


@router.get("/get-words", response_model=list[WordOut], name="vocabulary:get-words")
async def get_words(
    words: Annotated[list[WordOut] | None, Depends(search.search_simplified_words)]
) -> list[WordOut] | Response:
    if words is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error_message": "Words not found"})
    return words


@router.get("/get-characters", response_model=list[CharacterOut], name="vocabulary:get-characters")
async def get_characters(
    characters: Annotated[list[CharacterOut], Depends(search.search_characters)]
) -> list[CharacterOut]:
    return characters
