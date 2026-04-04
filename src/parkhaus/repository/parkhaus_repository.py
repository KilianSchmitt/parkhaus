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
    
    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
        session: Session,
    ) -> Slice[Parkhaus]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter als Dictionary
        :param pageable: Anzahl Datensätze und Seitennummer
        :param session: Session für SQLAlchemy
        :return: Ausschnitt der gefundenen Parkhäuser
        :rtype: Slice[Parkhaus]
        """
        logger.debug("{}", suchparameter)
        if not suchparameter:
            return self._find_all(pageable=pageable, session=session)

        for key, value in suchparameter.items():
            if key == "name":
                return self._find_by_name(teil=value, pageable=pageable, session=session)
            if key == "plz":
                return self._find_by_plz(plz=value, pageable=pageable, session=session)
            if key == "ort":
                return self._find_by_ort(teil=value, pageable=pageable, session=session)
        return Slice(content=(), total_elements=0)
    
    def _find_all(self, pageable: Pageable, session: Session) -> Slice[Parkhaus]:
        statement: Final = (
            select(Parkhaus)
            .options(joinedload(Parkhaus.adresse))
            .offset(pageable.number * pageable.size)
            .limit(pageable.size)
        )
        parkhaeuser: Final = tuple(session.scalars(statement).unique())
        return Slice(content=parkhaeuser, total_elements=len(parkhaeuser))

    def _find_by_name(self, teil: str, pageable: Pageable, session: Session) -> Slice[Parkhaus]:
        statement: Final = (
            select(Parkhaus)
            .options(joinedload(Parkhaus.adresse))
            .where(Parkhaus.name.ilike(f"%{teil}%"))
            .offset(pageable.number * pageable.size)
            .limit(pageable.size)
        )
        parkhaeuser: Final = tuple(session.scalars(statement).unique())
        return Slice(content=parkhaeuser, total_elements=len(parkhaeuser))

    def _find_by_plz(self, plz: str, pageable: Pageable, session: Session) -> Slice[Parkhaus]:
        statement: Final = (
            select(Parkhaus)
            .options(joinedload(Parkhaus.adresse))
            .join(Parkhaus.adresse)
            .where(Adresse.plz == plz)
            .offset(pageable.number * pageable.size)
            .limit(pageable.size)
        )
        parkhaeuser: Final = tuple(session.scalars(statement).unique())
        return Slice(content=parkhaeuser, total_elements=len(parkhaeuser))

    def _find_by_ort(self, teil: str, pageable: Pageable, session: Session) -> Slice[Parkhaus]:
        statement: Final = (
            select(Parkhaus)
            .options(joinedload(Parkhaus.adresse))
            .join(Parkhaus.adresse)
            .where(Adresse.ort.ilike(f"%{teil}%"))
            .offset(pageable.number * pageable.size)
            .limit(pageable.size)
        )
        parkhaeuser: Final = tuple(session.scalars(statement).unique())
        return Slice(content=parkhaeuser, total_elements=len(parkhaeuser))