"""Pydantic-Modell für das Parkhaus."""
from decimal import Decimal
from typing import Final

from loguru import logger
from pydantic import ConfigDict, field_serializer

from parkhaus.entity.parkhaus import Parkhaus
from parkhaus.router.adresse_model import AdresseModel
from parkhaus.router.auto_model import AutoModel
from parkhaus.router.parkhaus_update_model import ParkhausUpdateModel


class ParkhausModel(ParkhausUpdateModel):
    """Pydantic-Modell für das Parkhaus."""

    adresse: AdresseModel
    """Die Adresse des Parkhauses."""

    autos: list[AutoModel]
    """Die Liste der Autos, die im Parkhaus geparkt sind."""
    @field_serializer("tarif_pro_stunde")
    def serialize_decimal(self, value: Decimal, _info):
        """Wandelt Decimal für JSON in einen String um."""
        return str(value)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Parkhaus am Schloss",
                "kapazitaet": 200,
                "tarif_pro_stunde": "12.50",
                "adresse": {
                    "plz": "76133",
                    "ort": "Karlsruhe",
                    "strasse": "Moltkestraße",
                    "hausnummer": "30",
                },
                "autos": [
                    {
                        "einfahrtszeit": "2026-03-30T12:00:00",
                        "kundentyp": "PREMIUM",
                    },
                    {
                        "kennzeichen": "KA-AB-5678",
                        "einfahrtszeit": "2026-03-30T13:00:00",
                        "kundentyp": "BASIS",
                    },
                ],
            },
        }
    )

    def to_parkhaus(self) -> Parkhaus:
        """Konvertierung in ein Parkhaus-Objekt für SQLAlchemy.

        :return: Parkhaus-Objekt für SQLAlchemy
        :rtype: Parkhaus
        """
        logger.debug("self={}", self)
        parkhaus_dict = self.to_dict()

        parkhaus: Final = Parkhaus(**parkhaus_dict)
        parkhaus.adresse = self.adresse.to_adresse()
        parkhaus.autos = [
            auto_model.to_auto() for auto_model in self.autos
        ]
        logger.debug("parkhaus={}", parkhaus)
        return parkhaus
