from httpx import HTTPStatusError
from fastapi import HTTPException
import pytest
from httpx import Response, Request
from unittest.mock import AsyncMock
from app.dependencies import fetch_data, post_data


@pytest.fixture
def mock_httpx_get(monkeypatch):
    async def mock_get(*args, **kwargs):
        mock_response = Response(200, json={"key": "value"})
        mock_response._request = Request('GET', args[0])
        return mock_response

    mock = AsyncMock(side_effect=mock_get)
    monkeypatch.setattr("httpx.AsyncClient.get", mock)
    return mock


@pytest.fixture
def mock_httpx_post(monkeypatch):
    async def mock_post(*args, **kwargs):
        mock_response = Response(200)
        mock_response._request = Request('POST', args[0])
        return mock_response

    mock = AsyncMock(side_effect=mock_post)
    monkeypatch.setattr("httpx.AsyncClient.post", mock)
    return mock


@pytest.mark.asyncio
async def test_fetch_data_success(mock_httpx_get):
    url = "https://python.test.bobdaytech.ru/api/v1/simple-answer"
    result = await fetch_data(url, "test", "test")
    assert result == {"key": "value"}
    mock_httpx_get.assert_awaited_once_with(url, auth=("test", "test"))


@pytest.mark.asyncio
async def test_fetch_data_http_error(mock_httpx_get):
    request = Request('GET', 'https://wrong.url')
    response = Response(404, request=request)
    mock_httpx_get.side_effect = HTTPStatusError(message="Not Found", request=request, response=response)
    with pytest.raises(HTTPException) as exc_info:
        await fetch_data("https://wrong.url", "test", "test")
    assert exc_info.value.status_code == 404
    assert "Not Found" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_post_data_success(mock_httpx_post):
    url = "https://python.test.bobdaytech.ru/api/v1/simple-answer"
    data = {"key": "value"}
    status_code = await post_data(url, data, "test", "test")
    assert status_code == 200
    mock_httpx_post.assert_awaited_once_with(url, json=data, auth=("test", "test"))