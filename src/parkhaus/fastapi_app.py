"""FastAPI App."""
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Final

from fastapi import FastAPI, Request, Response, status
from loguru import logger

from parkhaus.banner import banner
from parkhaus.config import dev_db_populate, dev_keycloak_populate
from parkhaus.config.dev.db_populate import db_populate
from parkhaus.config.dev.db_populate_router import router as db_populate_router
from parkhaus.config.dev.keycloak_populate import keycloak_populate
from parkhaus.config.dev.keycloak_populate_router import (
    router as keycloak_populate_router,
)
from parkhaus.graphql_api import graphql_router
from parkhaus.problem_details import create_problem_details
from parkhaus.repository.session_factory import engine
from parkhaus.router import (
    health_router,
    hello_router,
    parkhaus_router,
    parkhaus_write_router,
    shutdown_router,
)
from parkhaus.security.exceptions import AuthorizationError
from parkhaus.service import (
    NotFoundError,
    ParkingFacilityFullError,
    VersionOutdatedError,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

TEXT_PLAIN: Final = "text/plain"


# --------------------------------------------------------------------------------------
# S t a r t u p   u n d   S h u t d o w n
# --------------------------------------------------------------------------------------
# https://fastapi.tiangolo.com/advanced/events
# pylint: disable=redefined-outer-name
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029
    """DB neu laden, falls im dev-Modus, sowie Banner in der Konsole."""
    if dev_db_populate:
        db_populate()
    if dev_keycloak_populate:
        keycloak_populate()
    banner(app.routes)
    yield
    logger.info("Der Server wird heruntergefahren")
    logger.info("Connection-Pool fuer die DB wird getrennt.")
    engine.dispose()


app: FastAPI = FastAPI(lifespan=lifespan)

# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(hello_router, prefix="/rest")
app.include_router(parkhaus_router, prefix="/rest/parkhaeuser")
app.include_router(parkhaus_write_router, prefix="/rest/parkhaeuser")
app.include_router(health_router, prefix="/health")
app.include_router(shutdown_router, prefix="/admin")

if dev_db_populate:
    app.include_router(db_populate_router, prefix="/dev")
if dev_keycloak_populate:
    app.include_router(keycloak_populate_router, prefix="/dev")

# --------------------------------------------------------------------------------------
# G r a p h Q L
# --------------------------------------------------------------------------------------
app.include_router(graphql_router, prefix="/graphql")

# --------------------------------------------------------------------------------------
# E x c e p t i o n   H a n d l e r
# --------------------------------------------------------------------------------------
@app.exception_handler(AuthorizationError)
def authorization_error_handler(_request: Request, _err: AuthorizationError) -> Response:
    """Errorhandler für AuthorizationError.

    :param _err: AuthorizationError aus der Security-Schicht
    :return: Response mit Statuscode 401
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_403_FORBIDDEN)


@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """Errorhandler für NotFoundError.

    :param _err: NotFoundError aus der Geschäftslogik
    :return: Response mit Statuscode 404
    :rtype: Response
    """
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(ParkingFacilityFullError)
def parking_facility_full_error_handler(
    _request: Request,
    err: ParkingFacilityFullError
    ) -> Response:
    """Errorhandler für ParkingFacilityFullError.

    :param _err: ParkingFacilityFullError aus der Geschäftslogik
    :return: Response mit Statuscode 409
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(err)
    )


@app.exception_handler(VersionOutdatedError)
def version_outdated_error_handler(
    _request: Request,
    err: VersionOutdatedError,
) -> Response:
    """Exception-Handling für VersionOutdatedError.

    :param _err: Exception, falls die Versionsnummer zum Aktualisieren veraltet ist
    :return: Response mit Statuscode 412
    :rtype: Response
    """
    return create_problem_details(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(err),
    )

