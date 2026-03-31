"""Pydantic-Modell für die Adresse."""

from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints
from parkhaus.entity.adresse import Adresse

__all__ = ["AdresseModel"]


class AdresseModel(BaseModel):
    """Pydantic-Modell für die Adresse."""

    plz: Annotated[str, StringConstraints(pattern=r"^\d{5}$")]
    """Postleitzahl muss aus genau 5 Ziffern bestehen."""

    ort: Annotated[str, StringConstraints(max_length=64)]
    """Ort."""

    strasse: Annotated[str, StringConstraints(max_length=64)]
    """Straße."""

    hausnummer: Annotated[str, StringConstraints(max_length=10)]
    """Hausnummer."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "plz": "76133",
                "ort": "Karlsruhe",
                "strasse": "Moltkestraße",
                "hausnummer": "30",
            },
        }
    )

    def to_adresse(self) -> Adresse:
        """Konvertierung in ein Adresse-Objekt für SQLAlchemy.

        :return: Adresse-Objekt für SQLAlchemy
        :rtype: Adresse
        """
        adresse_dict = self.model_dump()
        adresse_dict["id"] = None
        adresse_dict["parkhaus_id"] = None

        return Adresse(**adresse_dict)
