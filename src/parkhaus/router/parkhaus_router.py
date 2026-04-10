"""ParkhausGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from parkhaus.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from parkhaus.router.dependencies import get_service
from parkhaus.security import RolesRequired, Role
from parkhaus.service import ParkhausDTO, ParkhausService
from parkhaus.repository import Pageable
from parkhaus.repository.slice import Slice
from parkhaus.router.page import Page

__all__: list[str] = ["parkhaus_router"]

parkhaus_router: Final = APIRouter(tags=["Lesen"])


@parkhaus_router.get(
    path="/{parkhaus_id}",
    dependencies=[Depends(RolesRequired([Role.ADMIN, Role.PATIENT]))]
)
def get_by_id(
    parkhaus_id: int,
    request: Request,
    service: Annotated[ParkhausService, Depends(get_service)],
):
    """Sucht ein Parkhaus anhand der ID."""
    logger.debug("parkhaus_id={}", parkhaus_id)

    parkhaus: Final = service.find_by_id(parkhaus_id=parkhaus_id)
    logger.debug("parkhaus={}", parkhaus)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)
        if version is not None:
            try:
                if int(version) == parkhaus.version:
                    return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            except ValueError:
                logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_parkhaus_to_dict(parkhaus),
        headers={ETAG: f'"{parkhaus.version}"'},
    )

@parkhaus_router.get("")
def get(
        request: Request,
        service: Annotated[ParkhausService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parameter.

    :param request: Injiziertes Request-Objekt von FastAPI bzw. Starlette
        mit Query-Parameter
    :param service: Injizierter Service für Geschäftslogik
    :return: Gefundene Parkhäuser als JSON-Response
    :rtype: JSONResponse
    :raises NotFoundError: Wenn kein Parkhaus gefunden wurde.
    """

    query_params: Final = request.query_params
    logger.debug("{}", query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    suchparameter.pop("page", None)
    suchparameter.pop("size", None)

    parkhaus_slice: Final = service.find(suchparameter=suchparameter, pageable=pageable)

    result: Final = _parkhaus_slice_to_page(parkhaus_slice, pageable)
    logger.debug("result={}", result)
    return JSONResponse(content=result)

def _parkhaus_slice_to_page(
    parkhaus_slice: Slice[ParkhausDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    parkhaus_dict: Final = tuple(
        _parkhaus_to_dict(parkhaus) for parkhaus in parkhaus_slice.content
    )
    page: Final = Page.create(
        content=parkhaus_dict,
        pageable=pageable,
        total_elements=parkhaus_slice.total_elements,
    )
    return asdict(obj=page)


def _parkhaus_to_dict(parkhaus: ParkhausDTO) -> dict[str, Any]:
    parkhaus_dict: Final = asdict(obj=parkhaus)
    parkhaus_dict.pop("version")
    parkhaus_dict["tarif_pro_stunde"] = str(parkhaus_dict["tarif_pro_stunde"])
    return parkhaus_dict
