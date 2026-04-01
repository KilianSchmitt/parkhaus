"""Pydantic-Modell für das Auto."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from parkhaus.entity.auto import Auto
from parkhaus.entity.kundentyp import Kundentyp


class AutoModel(BaseModel):
    """Pydantic-Modell für das Auto."""

    kennzeichen: Annotated[
        str, StringConstraints(pattern=r"^[A-Z]{1,3}-[A-Z]{1,2}-\d{1,4}$")
    ]
    """Das Kennzeichen im Format 'ABC-XY-1234'."""

    einfahrtszeit: datetime
    """Die Einfahrtszeit als ISO 8601 String."""

    kundentyp: Kundentyp
    """Der Kundentyp, entweder 'PREMIUM', 'BASIS' oder 'ANWOHNER'."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "kennzeichen": "KA-KS-1234",
                "einfahrtszeit": "2026-03-30T12:00:00",
                "kundentyp": "PREMIUM",
            },
        }
    )

    def to_auto(self) -> Auto:
        """Konvertierung in ein Auto-Objekt für SQLAlchemy.

        :return: Auto-Objekt für SQLAlchemy
        :rtype: Auto
        """
        auto_dict = self.model_dump()
        auto_dict["id"] = None
        auto_dict["parkhaus_id"] = None

        return Auto(**auto_dict)
