import base64
import os
from datetime import datetime
from typing import Tuple

from src.entities.AuthErrorResponse import AuthErrorResponse
from src.entities.AuthResponse import AuthResponse
from src.entities.AuthRequestDetails import AuthRequestDetails, AuthRequestHeaders, AuthRequestParams
from src.entities.RefreshRequestDetails import RefreshRequestDetails, RefreshRequestHeaders, RefreshRequestParams
from src.entities.SpotMeInternalError import SpotMeInternalError
from src.httpx_provider.httpx_provider import HttpxProvider


class Spotify:
    def __init__(self, client_id: str | None, client_secret: str | None, redirect_uri: str | None):
        self.CLIENT_ID = client_id or os.getenv("CLIENT_ID", "")
        self.CLIENT_SECRET = client_secret or os.getenv("CLIENT_SECRET")
        self.REDIRECT_URI = redirect_uri or os.getenv("REDIRECT_URI", "")
        self.AUTH_URL = "https://accounts.spotify.com/authorize"
        self.TOKEN_URL = "https://accounts.spotify.com/api/token"
        self.HTTPX = HttpxProvider()

    def get_login_url(self) -> str:
        c_id = f'client_id={self.CLIENT_ID}'
        r_type = 'response_type=code'
        r_uri = f'redirect_uri={self.REDIRECT_URI}'
        scope = 'scope=user-read-private%20user-read-currently-playing%20user-read-recently-played'
        dialog = 'show_dialog=true'
        url = f'{self.AUTH_URL}?{c_id}&{r_type}&{r_uri}&{scope}&{dialog}'
        return url

    async def auth(self, code: str) -> Tuple[int, (AuthResponse | AuthErrorResponse | SpotMeInternalError)]:
        stuff = {
            "error": "",
            "error_description": "str"
        }

        model = AuthErrorResponse(error="123")


        auth_request_details: AuthRequestDetails = self.__get_auth_details(code)
        code, response = await self.HTTPX.POST(
            url=auth_request_details.url,
            params=auth_request_details.params.model_dump(mode="json"),
            headers=auth_request_details.headers.model_dump(mode="json", by_alias=True)
        )
        new_error: AuthErrorResponse = AuthErrorResponse()
        if code == 200:
            response['expires_at'] = int(response['expires_in']) + int(datetime.now().timestamp())
            return code, AuthResponse(**response)
        elif code < 500:
            return code, AuthErrorResponse(**response)
        return code, SpotMeInternalError(**response)

    def __get_auth_details(self, code: str) -> AuthRequestDetails:
        headers: AuthRequestHeaders = AuthRequestHeaders(
            Authorization=f"Basic {self.__encoded_secret()}",
            **{'Content-Type': 'application/x-www-form-urlencoded'}
        )
        params: AuthRequestParams = AuthRequestParams(
            grant_type="authorization_code",
            code=code,
            redirect_uri=self.REDIRECT_URI
        )
        return AuthRequestDetails(
            headers=headers,
            params=params,
            url=self.TOKEN_URL
        )

    def __get_refresh_details(self, refresh_token: str) -> RefreshRequestDetails:
        headers: RefreshRequestHeaders = RefreshRequestHeaders(
            Authorization=self.__encoded_secret(),
            **{'Content-Type': 'application/x-www-form-urlencoded'}
        )
        params: RefreshRequestParams = RefreshRequestParams(
            grant_type="refresh_token",
            refresh_token=refresh_token
        )
        return RefreshRequestDetails(
            headers=headers,
            params=params,
            url=self.TOKEN_URL
        )

    def __encoded_secret(self) -> str:
        secret_bytes = f'{self.CLIENT_ID}:{self.CLIENT_SECRET}'.encode('utf-8')
        return (base64.b64encode(secret_bytes)).decode('utf-8')
