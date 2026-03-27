"""Entity-Klasse für die Adresse."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column

from parkhaus.entity.base import Base


class Adresse(Base):
    """Entity-Klasse für die Adresse."""

    __tablename__ = "adresse"

    plz: Mapped[str]
    """Die Postleitzahl."""

    ort: Mapped[str]
    """Der Ort."""

    strasse: Mapped[str]
    """Die Straße."""

    hausnummer: Mapped[str]
    """Die Hausnummer."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    parkhaus_id: Mapped[int] = mapped_column(ForeignKey("parkhaus.id"))
    """ID des zugehörigen Parkhauses als Fremdschlüssel in der DB-Tabelle."""

    def __repr__(self) -> str:
        """Ausgabe einer Adresse als String ohne die Parkhausdaten."""
        return (
            f"Adresse(id={self.id}, plz={self.plz}, ort={self.ort}, "
            f"strasse={self.strasse}, hausnummer={self.hausnummer})"
        )
