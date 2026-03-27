"""Entity-Klasse für Auto."""

from datetime import datetime

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column

from parkhaus.entity.base import Base
from parkhaus.entity.kundentyp import Kundentyp


class Auto(Base):
    """Entity-Klasse für Auto."""

    __tablename__ = "auto"

    kennzeichen: Mapped[str]
    """Das Kennzeichen."""

    einfahrtszeit: Mapped[datetime]
    """Die Einfahrtszeit."""

    kundentyp: Mapped[Kundentyp]
    """Der Kundentyp."""

    id: Mapped[int] = mapped_column(
        Identity(start=1000),
        primary_key=True,
    )
    """Die generierte ID gemäß der zugehörigen IDENTITY-Spalte."""

    parkhaus_id: Mapped[int] = mapped_column(ForeignKey("parkhaus.id"))
    """ID des zugehörigen Parkhauses als Fremdschlüssel in der DB-Tabelle."""
