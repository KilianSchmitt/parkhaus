"""Minimal FastAPI App."""

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger

from parkhaus.banner import banner
from parkhaus.config import db_url

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029
    """Lifespan context manager for startup and shutdown."""
    banner(app.routes)
    yield
    logger.info("Der Server wird heruntergefahren")


app: FastAPI = FastAPI(lifespan=lifespan)

app.add_middleware(GZipMiddleware, minimum_size=500)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Hello from parkhaus"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "db": db_url}
