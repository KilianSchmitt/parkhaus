# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

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
