"""ParkhausWriteRouter."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from parkhaus.router.dependencies import get_write_service
from parkhaus.router.parkhaus_model import ParkhausModel
from parkhaus.service.parkhaus_write_service import ParkhausWriteService

__all__ = ["parkhaus_write_router"]


parkhaus_write_router: Final = APIRouter(tags=["Schreiben"])


@parkhaus_write_router.post("")
def post(
    parkhaus_model: ParkhausModel,
    request: Request,
    service: Annotated[ParkhausWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um einen neuen Parkhaus anzulegen.

    :param parkhaus_model: Parkhausdaten als Pydantic-Model
    :param request: Injiziertes Request-Objekt von FastAPI mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    """
    logger.debug("parkhaus_model={}", parkhaus_model)
    parkhaus_dto: Final = service.create(parkhaus=parkhaus_model.to_parkhaus())
    logger.debug("parkhaus_dto={}", parkhaus_dto)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{parkhaus_dto.id}"},
    )


@parkhaus_write_router.delete("/{parkhaus_id}")
def delete(
    parkhaus_id: int,
    service: Annotated[ParkhausWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um ein Parkhaus zu löschen.

    :param parkhaus_id: Die ID des zu löschenden Parkhauses.
    :param request: Injiziertes Request-Objekt von FastAPI mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    """
    logger.debug("parkhaus_id={}", parkhaus_id)
    service.delete_by_id(parkhaus_id=parkhaus_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
