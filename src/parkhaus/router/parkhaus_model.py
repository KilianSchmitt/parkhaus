"""Pydantic-Modell für das Parkhaus."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from parkhaus.entity.parkhaus import Parkhaus
from parkhaus.router.adresse_model import AdresseModel
from parkhaus.router.auto_model import AutoModell


class ParkhausModel(BaseModel):
    """Pydantic-Modell für das Parkhaus."""

    name: Annotated[str, StringConstraints(max_length=64)]
    """Der Name des Parkhauses."""

    kapazitaet: Annotated[int, (ge=1)]
    """Die Anzahl der Parkplätze des Parkhauses."""

    tarif_pro_stunde: Annotated[Decimal, StringConstraints(ge=0)]
    """Der Tarif pro Stunde für das Parkhaus."""

    adresse: AdresseModel
    """Die Adresse des Parkhauses."""

    autos: list[AutoModell]
    """Die Liste der Autos, die im Parkhaus geparkt sind."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Parkhaus am Schloss",
                "kapazitaet": 200,
                "tarif_pro_stunde": 2.5,
                "adresse": {
                    "plz": "76133",
                    "ort": "Karlsruhe",
                    "strasse": "Moltkestraße",
                    "hausnummer": "30",
                },
                "autos": [
                    {
                        "kennzeichen": "KA-KS-1234",
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
        parkhaus_dict = self.model_dump()
        parkhaus_dict["id"] = None

        adresse_model = parkhaus_dict.pop("adresse")
        parkhaus_dict["adresse"] = adresse_model.to_adresse()

        autos_model = parkhaus_dict.pop("autos")
        parkhaus_dict["autos"] = [auto.to_auto() for auto in autos_model]

        return Parkhaus(**parkhaus_dict)
