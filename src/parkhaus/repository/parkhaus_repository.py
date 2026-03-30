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
