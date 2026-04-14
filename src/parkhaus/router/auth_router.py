"""Auth-Router für den Token-Endpunkt (wird für Integrationstests benötigt, um einen Token zu holen)."""
from typing import Annotated, Final

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from loguru import logger

from parkhaus.problem_details import create_problem_details
from parkhaus.security.dependencies import get_token_service
from parkhaus.security.exceptions import LoginError
from parkhaus.security.login_data import LoginData
from parkhaus.security.token_service import TokenService

__all__ = ["auth_router"]

auth_router: Final = APIRouter(tags=["Auth"])


@auth_router.post("/token")
def token(
    login_data: LoginData,
    service: Annotated[TokenService, Depends(get_token_service)],
) -> JSONResponse:
    """Liefert einen JWT-Token für Benutzername und Passwort.

    :param login_data: Benutzername und Passwort als JSON
    :param service: injizierter TokenService
    :return: JSON mit dem Access-Token unter dem Schlüssel "token"
    :rtype: JSONResponse
    """
    logger.debug("username={}", login_data.username)
    try:
        keycloak_token: Final = service.token(
            username=login_data.username,
            password=login_data.password,
        )
    except LoginError:
        return create_problem_details(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token: Final = keycloak_token.get("access_token")
    logger.debug("access_token={}", access_token)
    return JSONResponse(content={"token": access_token})

