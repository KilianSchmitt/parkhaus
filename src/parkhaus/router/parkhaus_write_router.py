"""ParkhausWriteRouter."""
from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from loguru import logger

from parkhaus.problem_details import create_problem_details
from parkhaus.router.constants import IF_MATCH, IF_MATCH_MIN_LEN
from parkhaus.router.dependencies import get_write_service
from parkhaus.router.parkhaus_model import ParkhausModel
from parkhaus.router.parkhaus_update_model import ParkhausUpdateModel
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


@parkhaus_write_router.put(
    "/{parkhaus_id}"
    )
def put(
    parkhaus_id: int,
    parkhaus_update_model: ParkhausUpdateModel,
    request: Request,
    service: Annotated[ParkhausWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um ein Parkhaus zu aktualisieren.

    :param parkhaus_id: Die ID des zu aktualisierenden Parkhauses.
    :param parkhaus_update_model: Die aktualisierten Parkhausdaten als Pydantic-Model.
    :param request: Injiziertes Request-Objekt von FastAPI mit der Request-URL
    :param service: Injizierter Service für Geschäftslogik
    :rtype: Response
    :raises ValidationError: Falls es bei Pydantic Validierungsfehler gibt
    """
    if_match_value: Final = request.headers.get(IF_MATCH)
    logger.debug(
        "parkhaus_id={}, if_match={}, parkhaus_update_model={}",
        parkhaus_id,
        if_match_value,
        parkhaus_update_model
    )

    if if_match_value is None:
        return create_problem_details(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        )

    if (
        len(if_match_value) < IF_MATCH_MIN_LEN
        or not if_match_value.startswith('"')
        or not if_match_value.endswith('"')
    ):
        return create_problem_details(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    version: Final = if_match_value[1:-1]
    try:
        version_int: Final = int(version)
    except ValueError:
        return Response(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
        )

    parkhaus: Final = parkhaus_update_model.to_parkhaus()
    parkhaus_modified: Final = service.update(
        parkhaus_id=parkhaus_id,
        parkhaus=parkhaus,
        version=version_int
    )
    logger.debug("parkhaus_modified={}", parkhaus_modified)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{parkhaus_modified.version}"'},
    )
