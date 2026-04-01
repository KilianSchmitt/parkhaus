"""Entity-Klasse für Parkhausdaten."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Self

from sqlalchemy import Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from parkhaus.entity.adresse import Adresse
from parkhaus.entity.auto import Auto
from parkhaus.entity.base import Base


class Parkhaus(Base):
    """Entity-Klasse für Parkhausdaten."""

    __tablename__ = "parkhaus"

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    name: Mapped[str]
    """Der Name des Parkhauses."""

    kapazitaet: Mapped[int]
    """Die Anzahl der Parkplätze des Parkhauses."""

    tarif_pro_stunde: Mapped[Decimal]
    """Der Tarif pro Stunde für das Parkhaus."""

    adresse: Mapped[Adresse] = relationship(
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Die in einer 1:1-Beziehung referenzierte Adresse des Parkhauses."""

    autos: Mapped[list[Auto]] = relationship(cascade="save-update, delete")
    """Die in einer 1:N-Beziehung referenzierten Autos."""

    version: Mapped[int] = mapped_column(nullable=False, default=0)
    """Die Versionsnummer für optimistische Synchronisation."""

    erzeugt: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
    """Der Zeitstempel für das initiale INSERT in die DB-Tabelle."""

    aktualisiert: Mapped[datetime | None] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
        default=None,
    )

    __mapper_args__ = {"version_id_col": "version"}

    def set(self, parkhaus: Self) -> None:
        """Aktualisiert die Attribute des aktuellen Parkhaus-Objekts.

        :param parkhaus: Das Parkhaus-Objekt mit den aktuellen Daten.
        :type parkhaus: Self
        """
        self.name = parkhaus.name
        self.kapazitaet = parkhaus.kapazitaet
        self.tarif_pro_stunde = parkhaus.tarif_pro_stunde

    def __eq__(self, other: Any) -> bool:
        """Vergleich von Parkhaus-Objekten anhand der ID.

        :param other: Das zu vergleichende Objekt.
        :return: True, wenn die IDs gleich sind, sonst False.
        """
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        """Hash-Wert für Parkhaus-Objekte basierend auf der ID."""
        return hash(self.id) if self.id is not None else hash(type(self))

    def __repr__(self) -> str:
        """Ausgabe eines Parkhauses als String ohne die Adress- und Autodaten."""
        return (
            f"Parkhaus(id={self.id}, name={self.name}, "
            f"kapazitaet={self.kapazitaet}, tarif_pro_stunde={self.tarif_pro_stunde}, "
            f"erzeugt={self.erzeugt}, aktualisiert={self.aktualisiert})"
        )
