"""Module fuer die REST-Schnittstelle."""

from collections.abc import Sequence

from parkhaus.router.health_router import liveness, readiness
from parkhaus.router.health_router import router as health_router
from parkhaus.router.hello_router import hello_router
from parkhaus.router.parkhaus_router import get_by_id, parkhaus_router
from parkhaus.router.shoutdown_router import router as shutdown_router
from parkhaus.router.shoutdown_router import shutdown

__all__: Sequence[str] = [
    "get_by_id",
    "health_router",
    "hello_router",
    "liveness",
    "parkhaus_router",
    "readiness",
    "shutdown",
    "shutdown_router",
]
