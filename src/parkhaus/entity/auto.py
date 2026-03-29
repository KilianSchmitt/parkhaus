"""Entity-Klasse für Auto."""

from datetime import datetime

from sqlalchemy import ForeignKey, Identity, String
from sqlalchemy.orm import Mapped, mapped_column

from parkhaus.entity.base import Base


class Auto(Base):
    """Entity-Klasse für Auto."""

    __tablename__ = "auto"

    kennzeichen: Mapped[str]
    """Das Kennzeichen."""

    einfahrtszeit: Mapped[datetime]
    """Die Einfahrtszeit."""

    kundentyp: Mapped[str] = mapped_column(String(10))
    """Der Kundentyp als String ('PREMIUM', 'BASIS', 'ANWOHNER')."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    parkhaus_id: Mapped[int] = mapped_column(ForeignKey("parkhaus.id"))
    """ID des zugehörigen Parkhauses als Fremdschlüssel in der DB-Tabelle."""

    def __repr__(self) -> str:
        """Ausgabe eines Autos als String ohne die Parkhausdaten."""
        return (
            f"Auto(id={self.id}, kennzeichen={self.kennzeichen}, "
            f"einfahrtszeit={self.einfahrtszeit}, kundentyp={self.kundentyp})"
        )
