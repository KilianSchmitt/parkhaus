"""Geschäftslogik zum Schreiben von Parkhaus-Daten."""
import re
from typing import Final

from loguru import logger

from parkhaus.entity.parkhaus import Parkhaus
from parkhaus.repository.parkhaus_repository import ParkhausRepository
from parkhaus.repository.session_factory import Session
from parkhaus.service import NotFoundError
from parkhaus.service.exceptions import ParkingFacilityFullError, VersionOutdatedError
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

    def delete_by_id(self, parkhaus_id: int) -> None:
        """Ein Parkhaus anand der ID löschen.

        :param parkhaus_id: Die ID des zu löschenden Parkhauses.
        """
        logger.debug("parkhaus_id={}", parkhaus_id)
        with Session() as session:
            self.repo.delete_by_id(parkhaus_id, session=session)
            session.commit()

    def update(self, parkhaus: Parkhaus, parkhaus_id: int, version: int) -> ParkhausDTO:
        """Ein bestehendes Parkhaus aktualisieren.

        :param parkhaus: Das zu aktualisierende Parkhaus.
        :return: Das aktualisierte Parkhaus als DTO oder None.
        """
        logger.debug("parkhaus_id={}, version={}, {}", parkhaus_id, version, parkhaus)
        with Session() as session:
            if (
                parkhaus_db := self.repo.find_by_id(
                    parkhaus_id=parkhaus_id, session=session
                )
            ) is None:
                raise NotFoundError(parkhaus_id)
            if parkhaus_db.version != version:
                raise VersionOutdatedError(version=version)

            if parkhaus.kapazitaet < len(parkhaus_db.autos):
                raise ParkingFacilityFullError(
                    parkhaus_id=parkhaus.id,
                    kapazitaet=parkhaus.kapazitaet
                )

            parkhaus_db.set(parkhaus)
            if (
                parkhaus_updated := self.repo.update(parkhaus_db, session=session)
            ) is None:
                raise NotFoundError(parkhaus_id)
            parkhaus_dto: Final = ParkhausDTO(parkhaus_updated)
            logger.debug("{}", parkhaus_dto)

            session.commit()
            parkhaus_dto.version += 1
            return parkhaus_dto
