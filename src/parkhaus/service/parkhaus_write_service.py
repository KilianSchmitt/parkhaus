"""Geschäftslogik zum Schreiben von Parkhaus-Daten."""
from typing import Final

from loguru import logger

from parkhaus.entity.parkhaus import Parkhaus
from parkhaus.repository.parkhaus_repository import ParkhausRepository
from parkhaus.repository.session_factory import Session
from parkhaus.service.exceptions import ParkingFacilityFullError
from parkhaus.service.parkhaus_dto import ParkhausDTO

__all__: list[str] = ["ParkhausWriteService"]


class ParkhausWriteService:
    """Service-Klasse mit Geschäftslogik von Parkhaus-Daten."""

    def __init__(self, repo: ParkhausRepository) -> None:
        """Konstruktor für ParkhausWriteService.

        :param repo: Das Repository für Parkhaus-Daten.
        """
        self.repo: ParkhausRepository = repo

    def create(self, parkhaus: Parkhaus) -> ParkhausDTO:
        """Ein neues Parkhaus erstellen.

        :param parkhaus: Das anzulegende Parkhaus ohne ID.
        :return: Das angelegte Parkhaus als DTO.
        """
        logger.debug(
            "parkhaus={}, adresse={}, autos={}",
            parkhaus,
            parkhaus.adresse,
            parkhaus.autos,
        )

        if parkhaus.kapazitaet < len(parkhaus.autos):
            raise ParkingFacilityFullError(
                parkhaus_id=parkhaus.id,
                kapazitaet=parkhaus.kapazitaet
            )

        with Session() as session:
            parkhaus_db: Final = self.repo.create(
                parkhaus=parkhaus,
                session=session
            )
            parkhaus_dto: Final = ParkhausDTO(parkhaus_db)
            session.commit()

        logger.debug("parkhaus_dto={}", parkhaus_dto)
        return parkhaus_dto
