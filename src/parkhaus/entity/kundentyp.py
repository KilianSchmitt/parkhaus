"""Enum für Kundentyp."""

from enum import StrEnum

import strawberry


@strawberry.enum
class Kundentyp(StrEnum):
    """Enum für die verschiedenen Kundentypen."""

    PREMIUM = "PREMIUM"
    """Premiumkunde."""

    BASIS = "BASIS"
    """Basiskunde."""

    ANWOHNER = "ANWOHNER"
    """Anwohner."""
