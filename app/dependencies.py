import httpx
from .config import get_config
from fastapi import HTTPException

config = get_config()
BASE_URL_GET = config['API']['URL_GET']
BASE_URL_POST = config['API']['URL_POST']
USERNAME = config['API']['USERNAME']
PASSWORD = config['API']['PASSWORD']


async def fetch_data(url: str, username: str, password: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, auth=(username, password))
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except httpx.RequestError as exc:
            print(f"Failed to send a request due to a network issue: {exc}")
            raise HTTPException(status_code=500, detail="Failed to send a request due to a network issue")
        except httpx.HTTPError as exc:
            print(f"An HTTP error occurred: {exc}")
            raise HTTPException(status_code=500, detail="An HTTP error occurred")


async def post_data(url: str, data: dict, username: str, password: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, auth=(username, password))
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except httpx.RequestError as exc:
            print(f"Failed to send a request due to a network issue: {exc}")
            raise HTTPException(status_code=500, detail="Failed to send a request due to a network issue")
        except httpx.HTTPError as exc:
            print(f"An HTTP error occurred: {exc}")
            raise HTTPException(status_code=500, detail="An HTTP error occurred")
