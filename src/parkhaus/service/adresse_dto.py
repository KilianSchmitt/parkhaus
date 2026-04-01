"""DTO-Klasse für die Adresse."""

from dataclasses import dataclass

import strawberry

from parkhaus.entity import Adresse


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class AdresseDTO:
    """DTO-Klasse für die Adresse, insbesondere ohne Decorators für SQLAlchemy."""

    plz: str
    ort: str
    strasse: str
    hausnummer: str

    def __init__(self, adresse: Adresse) -> None:
        """Initialisierung von AdresseDTO durch ein Entity-Objekt von Adresse.

        :param adresse: Adresse-Objekt mit Decorators für SQLAlchemy
        """
        self.plz = adresse.plz
        self.ort = adresse.ort
        self.strasse = adresse.strasse
        self.hausnummer = adresse.hausnummer
