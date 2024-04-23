from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.entities.AuthErrorResponse import AuthErrorResponse
from src.entities.AuthResponse import AuthResponse
from src.entities.LoginUrlResponse import LoginUrlResponse
from src.entities.SpotMeInternalError import SpotMeInternalError
from src.spotify.spotify import Spotify


spotify = Spotify(None, None, None)

controller = APIRouter(
    prefix="/spotify",
    tags=["Spotify"],
    responses={
        500: {"model": SpotMeInternalError},
    },
    dependencies=[],
)


@controller.get('/login', tags=['Spotify'], response_model=LoginUrlResponse)
async def login():
    return LoginUrlResponse(url=spotify.get_login_url())


@controller.get(
    '/callback',
    tags=['Spotify'],
    response_model=AuthResponse,
    responses={
        400: {"model": AuthErrorResponse},
        500: {"model": SpotMeInternalError}
    }
                )
async def callback(
    code: Optional[str | None] = None,
    error: Optional[str | None] = None,
    state: Optional[str | None] = None
) -> JSONResponse:
    if error:
        return JSONResponse(
            status_code=401,
            content=SpotMeInternalError(
                status=401,
                errors=[error],
                description="Could not authorize Spotify Login"
            ).model_dump(mode="json")
        )
    code, token_details = await spotify.auth(code)
    return JSONResponse(status_code=code, content=token_details.model_dump(mode="json"))
