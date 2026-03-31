"""DTO-Klasse für Parkhausdaten."""

from dataclasses import dataclass
from decimal import Decimal

import strawberry

from parkhaus.entity import Parkhaus
from parkhaus.service.adresse_dto import AdresseDTO

__all__ = ["ParkhausDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type
class ParkhausDTO:
    """DTO-Klasse für aus gelesene oder gespeicherte Parkhausdaten: ohne Decorators."""

    id: int
    version: int
    name: str
    kapazitaet: int
    tarif_pro_stunde: Decimal
    adresse: AdresseDTO

    def __init__(self, parkhaus: Parkhaus) -> None:
        """Initialisierung von ParkhausDTO durch ein Entity-Objekt von Parkhaus.

        :param parkhaus: Parkhaus-Objekt mit Decorators zu SQLAlchemy
        """
        parkhaus_id = parkhaus.id
        self.id = parkhaus_id if parkhaus_id is not None else -1
        self.version = parkhaus.version
        self.name = parkhaus.name
        self.kapazitaet = parkhaus.kapazitaet
        self.tarif_pro_stunde = parkhaus.tarif_pro_stunde
        self.adresse = AdresseDTO(parkhaus.adresse)
