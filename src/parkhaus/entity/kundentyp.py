"""Enum für Kundentyp."""

from enum import StrEnum

import strawberry

@strawberry.enum
class Kundentyp(StrEnum):
    """Enum für die verschiedenen Kundentypen."""

    PREMIUM = "P"
    """Premiumkunde."""

    BASIS = "B"
    """Basiskunde."""

    ANWOHNER = "A"
    """Anwohner."""
