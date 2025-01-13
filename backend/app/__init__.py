from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router  # Import the router containing all endpoints
from backend.data_ingestion.ingestion import ingest_articles

from contextlib import asynccontextmanager, AbstractAsyncContextManager

from dotenv import load_dotenv

load_dotenv()

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    @asynccontextmanager
    async def lifespan(the_app):
        print("Startup things...")
        ingest_articles()
        yield
        print("Shutdown things...")

    app = FastAPI(lifespan=lifespan)

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