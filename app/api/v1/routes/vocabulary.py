from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from app.api.dependencies import search
from app.domain.vocabulary.combined import CharacterOut, WordOut

router = APIRouter()


@router.get("/get-character", response_model=CharacterOut, name="vocabulary:get-character")
async def get_character(
    character: Annotated[CharacterOut | None, Depends(search.search_character)]
) -> CharacterOut | Response:
    if character is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error_message": "Character not found"})
    return character


@router.get("/get-word", response_model=list[WordOut], name="vocabulary:get-word")
async def get_word(
    words: Annotated[list[WordOut] | None, Depends(search.search_simplified_word)]
) -> list[WordOut] | Response:
    if words is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error_message": "Word not found"})
    return words
