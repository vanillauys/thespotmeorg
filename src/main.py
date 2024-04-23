from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller import spotify_controller

TAGS_METADATA = [
    {
        "name": "Testing",
        "description": "Test endpoints",
    },
    {
        "name": "Spotify",
        "description": "Spotify Web API",
        "externalDocs": {
            "description": "Spotify Web API",
            "url": "https://developer.spotify.com/documentation/web-api"
        }
    },
]

app = FastAPI(
    title="Spot Me Org API",
    description="Spot Me API Collection",
    version="0.0.0",
    terms_of_service="",
    contact={
        "name": "The Spot Me Org",
        "url": "https://vanillauys.vercel.app",
        "email": "wihan@duck.com",
    },
    openapi_tags=TAGS_METADATA,
    openapi_url="/openapi.json",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spotify_controller.controller)


@app.get('/', tags=['Testing'])
async def info():
    """
    ### Basic route to test functionality.
    """
    return {"hello": "world"}
