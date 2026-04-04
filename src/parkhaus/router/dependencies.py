"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from parkhaus.repository.parkhaus_repository import ParkhausRepository
from parkhaus.service.parkhaus_service import ParkhausService
from parkhaus.service.parkhaus_write_service import ParkhausWriteService


def get_repository() -> ParkhausRepository:
    """Factory-Funktion für ParkhausRepository.

    :return: Das Repository
    :rtype: ParkhausRepository
    """
    return ParkhausRepository()


def get_service(
    repo: Annotated[ParkhausRepository, Depends(get_repository)],
) -> ParkhausService:
    """Factory-Funktion für ParkhausService."""
    return ParkhausService(repo=repo)


def get_write_service(
    repo: Annotated[ParkhausRepository, Depends(get_repository)],
) -> ParkhausWriteService:
    """Factory-Funktion für ParkhausWriteService."""
    return ParkhausWriteService(repo=repo)
