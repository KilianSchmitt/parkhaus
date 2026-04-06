"""Modul für die GraphQL-Schnittstelle."""

from parkhaus.graphql_api.schema import Query, graphql_router

__all__ = [
    "graphql_router",
    "Query",
]
