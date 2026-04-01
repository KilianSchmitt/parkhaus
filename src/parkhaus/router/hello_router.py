"""Simple Hello Router."""
from typing import Final

from fastapi import APIRouter

__all__: list[str] = ["hello_router"]


hello_router: Final = APIRouter(tags=["Lesen"])


@hello_router.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Hello from parkhaus"}
