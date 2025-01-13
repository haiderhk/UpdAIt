from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router  # Import the router containing all endpoints
from dotenv import load_dotenv

load_dotenv()

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI()

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Include routes
    app.include_router(router)

    return app