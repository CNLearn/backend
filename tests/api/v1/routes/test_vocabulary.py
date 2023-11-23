from typing import Any
from urllib.parse import urlencode

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response


@pytest.mark.asyncio
async def test_search_word(
    client: AsyncClient,
    app: FastAPI,
) -> None:
    search_url: str = app.url_path_for("vocabulary:get-words")
    query_params: dict[str, str] = {"simplified_words": "鸦雀无声"}
    search_url += "?" + urlencode(query_params)
    response: Response = await client.get(
        url=search_url,
    )
    json_response: list[dict[str, Any]] = response.json()

    assert response.status_code == 200
    assert len(json_response) == 1
    assert json_response[0]["simplified"] == "鸦雀无声"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("include_words", "n_words"),
    [
        pytest.param(False, 0, id="without requesting words"),
        pytest.param(True, 1, id="with requesting words"),
    ],
)
async def test_search_character(
    # the following are pytest parameters
    include_words: bool,
    n_words: int,
    # the following are root conftest fixtures
    client: AsyncClient,
    app: FastAPI,
) -> None:
    # http://localhost:8000/api/v1/vocabulary/get-character?character=%E9%B8%A6&words=true'
    search_url: str = app.url_path_for("vocabulary:get-characters")
    query_params: dict[str, str | bool] = {"characters": "鸦", "include_words": include_words}
    search_url += "?" + urlencode(query_params)
    response: Response = await client.get(
        url=search_url,
    )
    json_response: list[dict[str, Any]] = response.json()

    assert response.status_code == 200
    assert json_response[0]["character"] == "鸦"
    assert len(json_response[0]["words"]) == n_words
