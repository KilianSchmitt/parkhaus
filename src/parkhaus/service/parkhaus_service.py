"""Geschäftslogik zum Lesen von Parkhausdaten."""

from typing import Final

from loguru import logger

from parkhaus.repository import ParkhausRepository, Session
from parkhaus.service.exceptions import NotFoundError
from parkhaus.service.parkhaus_dto import ParkhausDTO

__all__: list[str] = ["ParkhausService"]


class ParkhausService:
    """Service-Klasse mit Geschäftslogik für Parkhäuser."""

    def __init__(self, repo: ParkhausRepository) -> None:
        """Konstruktor mit Abhängigkeit zu ParkhausRepository."""
        self.repo = repo

    def find_by_id(self, parkhaus_id: int) -> ParkhausDTO:
        """Findet ein Parkhaus anhand der ID.

        :param parkhaus_id: ID für die Suche
        :return: Gefundenes Parkhaus als DTO
        :rtype: ParkhausDTO
        :raises NotFoundError: Wenn kein Parkhaus gefunden wurde.
        """
        logger.debug("parkhaus_id={}", parkhaus_id)

        with Session() as session:
            if (
                parkhaus := self.repo.find_by_id(
                    parkhaus_id=parkhaus_id, session=session
                )
            ) is None:
                message: Final = f"Kein Parkhaus mit der ID {parkhaus_id}"
                logger.debug("NotFoundError: {}", message)
                raise NotFoundError(parkhaus_id=parkhaus_id)
            parkhaus_dto: Final = ParkhausDTO(parkhaus)
            session.commit()

        logger.debug("{}", parkhaus_dto)
        return parkhaus_dto
