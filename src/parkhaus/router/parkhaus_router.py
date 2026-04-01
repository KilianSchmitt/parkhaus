"""ParkhausGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from parkhaus.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from parkhaus.router.dependencies import get_service
from parkhaus.service import ParkhausDTO, ParkhausService

__all__: list[str] = ["parkhaus_router"]

parkhaus_router: Final = APIRouter(tags=["Lesen"])


@parkhaus_router.get(path="/{parkhaus_id}")
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


def _parkhaus_to_dict(parkhaus: ParkhausDTO) -> dict[str, Any]:
    parkhaus_dict: Final = asdict(obj=parkhaus)
    parkhaus_dict.pop("version")
    return parkhaus_dict
