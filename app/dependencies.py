import httpx
from .config import get_config
from fastapi import HTTPException
from .logger import logger

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
            logger.info(f"Data fetched successfully from {url}")
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP status error occurred while fetching data: {exc}")
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except httpx.RequestError as exc:
            logger.error(f"Request error: {exc}")
            raise HTTPException(status_code=500, detail="Network issue")
        except httpx.HTTPError as exc:
            logger.error(f"HTTP error: {exc}")
            raise HTTPException(status_code=500, detail="HTTP error occurred")


async def post_data(url: str, data: dict, username: str, password: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, auth=(username, password))
            response.raise_for_status()
            logger.info(f"Data posted successfully to {url}")
            return response.status_code
        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP status error occurred while posting data: {exc}")
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except httpx.RequestError as exc:
            logger.error(f"Request error: {exc}")
            raise HTTPException(status_code=500, detail="Network issue")
        except httpx.HTTPError as exc:
            logger.error(f"HTTP error: {exc}")
            raise HTTPException(status_code=500, detail="HTTP error occurred")
