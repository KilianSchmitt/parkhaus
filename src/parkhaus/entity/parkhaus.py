"""Entity-Klasse für Parkhausdaten."""

from typing import TYPE_CHECKING

from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from parkhaus.entity.base import Base

if TYPE_CHECKING:
    from parkhaus.entity.adresse import Adresse
    from parkhaus.entity.auto import Auto


class Parkhaus(Base):
    """Entity-Klasse für Parkhausdaten."""

    __tablename__ = "parkhaus"

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    name: Mapped[str]
    """Der Name des Parkhauses."""

    kapazitaet: Mapped[int]
    """Die Anzahl der Parkplätze des Parkhauses."""

    tarif_pro_stunde: Mapped[float]
    """Der Tarif pro Stunde für das Parkhaus."""

    adresse: Mapped[Adresse] = relationship(
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Die Adresse des Parkhauses."""

    autos: Mapped[list[Auto]] = relationship(cascade="save-update, delete")
    """Die in einer 1:N-Beziehung referenzierten Autos."""

    def __repr__(self) -> str:
        """Ausgabe eines Parkhauses als String ohne die Adresse- und Autodaten."""
        return (
            f"Parkhaus(id={self.id}, name={self.name}, "
            f"kapazitaet={self.kapazitaet}, tarif_pro_stunde={self.tarif_pro_stunde})"
        )
