"""Pydantic-Modell für das Parkhaus."""

from decimal import Decimal
from typing import Annotated, Final

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_serializer

from parkhaus.entity.parkhaus import Parkhaus
from parkhaus.router.adresse_model import AdresseModel
from parkhaus.router.auto_model import AutoModel


class ParkhausModel(BaseModel):
    """Pydantic-Modell für das Parkhaus."""

    name: Annotated[str, StringConstraints(max_length=64)]
    """Der Name des Parkhauses."""

    kapazitaet: Annotated[int, Field(ge=1)]
    """Die Anzahl der Parkplätze des Parkhauses."""

    tarif_pro_stunde: Annotated[Decimal, Field(ge=0)]
    """Der Tarif pro Stunde für das Parkhaus."""

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
        """Konvertierung in ein Parkhaus-Objekt für SQLAlchemy."""
        return Parkhaus(
            id=None,
            name=self.name,
            kapazitaet=self.kapazitaet,
            tarif_pro_stunde=self.tarif_pro_stunde,
            adresse=self.adresse.to_adresse(),
            autos=[auto.to_auto() for auto in self.autos]
        )
