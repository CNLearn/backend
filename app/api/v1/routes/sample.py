from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_words() -> Any:
    """
    Returns a list of words.
    """
    words = [
        {"id": 1, "simplified": "好", "pinyin": "hǎo", "definitions": "good"},
        {"id": 2, "simplified": "不", "pinyin": "bù", "definitions": "no"},
    ]
    return words
