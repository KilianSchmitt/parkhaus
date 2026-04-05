"""Pydantic-Modell zum Aktualisieren von Parkhausdaten."""

from decimal import Decimal
from typing import Annotated, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_serializer

from parkhaus.entity.parkhaus import Parkhaus

__all__ = ["ParkhausUpdateModel"]


class ParkhausUpdateModel(BaseModel):
    """Pydantic-Modell zum Aktualisieren von Parkhausdaten."""

    name: Annotated[str, StringConstraints(max_length=64)]
    """Der Name des Parkhauses."""

    kapazitaet: Annotated[int, Field(ge=1)]
    """Die Anzahl der Parkplätze des Parkhauses."""

    tarif_pro_stunde: Annotated[Decimal, Field(ge=0)]
    """Der Tarif pro Stunde für das Parkhaus."""

    @field_serializer("tarif_pro_stunde")
    def serialize_decimal(self, value: Decimal, _info):
        """Wandelt Decimal für JSON in einen String um."""
        return str(value)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Parkhaus am Schloss",
                "kapazitaet": 250,
                "tarif_pro_stunde": "15.00",
            },
        }
    )

    def to_dict(self) -> dict[str, Any]:
        """Konvertierung der primitiven Attribute in ein Dictionary.

        :return: Dictionary mit den primitiven Parkhaus-Attributen
        :rtype: dict[str, Any]
        """
        parkhaus_dict = self.model_dump()
        # Initialisierung der Relationen/Metadaten auf None oder leere Listen
        parkhaus_dict["id"] = None
        parkhaus_dict["adresse"] = None
        parkhaus_dict["autos"] = []
        parkhaus_dict["erzeugt"] = None
        parkhaus_dict["aktualisiert"] = None

        return parkhaus_dict

    def to_parkhaus(self) -> Parkhaus:
        """Konvertierung in ein Parkhaus-Objekt für SQLAlchemy.

        :return: Parkhaus-Objekt für SQLAlchemy
        :return: Parkhaus
        """
        logger.debug("self={}", self)
        parkhaus_dict = self.to_dict()

        parkhaus = Parkhaus(**parkhaus_dict)
        logger.debug("parkhaus={}", parkhaus)
        return parkhaus
