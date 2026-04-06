"""Repository für persistente Parkhaus-Daten."""
from typing import Final

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from parkhaus.entity.parkhaus import Parkhaus


class ParkhausRepository:
    """Repository-Klasse mit CRUD-Methoden für die Entity-Klasse Parkhaus."""

    def find_by_id(self, parkhaus_id: int | None, session: Session) -> Parkhaus | None:
        """Suche mit der Parkhaus-ID.

        :param parkhaus_id: Die ID des gesuchten Parkhauses.
        :param session: Session für SQLAlchemy.
        :return: Das gefundene Parkhaus oder None.
        :rtype: Parkhaus | None
        """
        logger.debug("parkhaus_id={}", parkhaus_id)  # NOSONAR

        if parkhaus_id is None:
            return None

        statement: Final = (
            select(Parkhaus)
            .options(joinedload(Parkhaus.adresse))
            .where(Parkhaus.id == parkhaus_id)
        )
        parkhaus: Final = session.scalar(statement)

        logger.debug("parkhaus={}", parkhaus)
        return parkhaus

    def create(self, parkhaus: Parkhaus, session: Session) -> Parkhaus:
        """Neues Parkhaus anlegen.

        :param parkhaus: Das anzulegende Parkhaus.
        :param session: Session für SQLAlchemy.
        :return: Das angelegte Parkhaus mit ID.
        :rtype: Parkhaus
        """
        logger.debug(
            "parkhaus={}, parkhaus.adresse={}, parkhaus.autos={}",
            parkhaus,
            parkhaus.adresse,
            parkhaus.autos,
        )
        session.add(parkhaus)
        session.flush(objects=[parkhaus])
        logger.debug("parkhaus_id={}", parkhaus.id)
        return parkhaus

    def delete_by_id(self, parkhaus_id: int, session: Session) -> None:
        """Löschen eines Parkhauses mit der ID.

        :param parkhaus_id: Die ID des zu löschenden Parkhauses.
        :param session: Session für SQLAlchemy.
        """
        logger.debug("parkhaus_id={}", parkhaus_id)

        if (parkhaus := self.find_by_id(parkhaus_id, session)) is None:
            return
        session.delete(parkhaus)
        logger.debug("ok")

    def update(self, parkhaus: Parkhaus, session: Session) -> Parkhaus | None:
        """Aktualisieren eines bestehenden Parkhauses.

        :param parkhaus: Das zu aktualisierende Parkhaus.
        :param session: Session für SQLAlchemy.
        :return: Das aktualisierte Parkhaus.
        :rtype: Parkhaus
        """
        logger.debug("parkhaus={}", parkhaus)

        if (
            parkhaus_db := self.find_by_id(parkhaus.id, session)
        ) is None:
            return None

        logger.debug("parkhaus_db={}", parkhaus_db)
        return parkhaus_db
