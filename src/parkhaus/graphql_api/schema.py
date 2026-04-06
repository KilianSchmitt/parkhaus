"""Schema für GraphQL durch Strawberry."""

import strawberry
from fastapi import Request
from loguru import logger
from sqlalchemy.util.typing import Final
from strawberry.fastapi import GraphQLRouter

from parkhaus.config.graphql import graphql_ide
from parkhaus.repository import ParkhausRepository
from parkhaus.service import ParkhausDTO, ParkhausService
from parkhaus.service.exceptions import NotFoundError

__all__ = ["graphql_router"]

_repo: Final = ParkhausRepository()
_service: Final = ParkhausService(repo=_repo)


@strawberry.type
class Query:
    """Queries, um Parkhausdaten zu lesen."""

    @strawberry.field
    def parkhaus(self, parkhaus_id: strawberry.ID) -> ParkhausDTO | None:
        """Daten zu einem Parkhaus.

        :param parkhaus_id: Die ID des Parkhauses
        :return: Gesuchtes Parkhaus
        :rtype: ParkhausDTO | None
        :raises NotFoundError: Falls kein Parkhaus gefunden wurde, wird zu GraphQLError
        """
        logger.debug("parkhaus_id={}", parkhaus_id)

        try:
            parkhaus_dto: Final = _service.find_by_id(parkhaus_id=int(parkhaus_id))
        except NotFoundError:
            return None
        logger.debug("parkhaus_dto={}", parkhaus_dto)
        return parkhaus_dto


schema: Final = strawberry.Schema(query=Query)


Context = dict[str, Request]


def get_context(request: Request) -> Context:
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema, context_getter=get_context, graphql_ide=graphql_ide
)
