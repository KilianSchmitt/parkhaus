"""Entity-Klasse für Parkhausdaten."""
from sqlalchemy.orm import Mapped, relationship

from parkhaus.entity.adresse import Adresse
from parkhaus.entity.auto import Auto
from parkhaus.entity.base import Base


class Parkhaus(Base):
    """Entity-Klasse für Parkhausdaten."""

    __tablename__ = "parkhaus"

    name: Mapped[str]
    """Der Name des Parkhauses."""

    kapazitaet: Mapped[int]
    """Die Anzahl der Parkplätze des Parkhauses."""

    traif_pro_stunde: Mapped[float]
    """Der Tarif pro Stunde für das Parkhaus."""

    adresse: Mapped[Adresse] = relationship(
        innerjoin=True,
        cascade="save-update, delete",
    )
    """Die Adresse des Parkhauses."""

    autos: Mapped[list[Auto]] = relationship(cascade="save-update, delete")
    """Die in einer 1:N-Beziehung referenzierten Autos."""
