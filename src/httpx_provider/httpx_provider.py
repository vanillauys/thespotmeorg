from typing import Optional, Tuple
import httpx

from src.entities.SpotMeInternalError import SpotMeInternalError


class HttpxProvider:
    def __init__(self):
        self.timeout = httpx.Timeout(read=20, write=20, connect=20, timeout=20)

    async def GET(
            self,
            url: str,
            params: Optional[dict | None] = None,
            headers: Optional[dict | None] = None
    ) -> Tuple[int, dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, params=params, headers=headers, timeout=self.timeout)
            return response.status_code, response.json()
        except Exception as err:
            return 500, SpotMeInternalError(
                status=500, errors=[str(err)],
                description=f"Could not send GET request to {url}"
            ).model_dump(mode="json")
    
    async def POST(
            self,
            url: str, params: Optional[dict | None] = None,
            headers: Optional[dict | None] = None
    ) -> Tuple[int, dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, params=params, headers=headers, timeout=self.timeout)
            return response.status_code, response.json()
        except Exception as err:
            return 500, SpotMeInternalError(
                status=500, errors=[str(err)],
                description=f"Could not send POST request to {url}"
            ).model_dump(mode="json")

