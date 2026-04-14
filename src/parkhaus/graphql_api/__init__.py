"""Modul für die GraphQL-Schnittstelle."""

from parkhaus.graphql_api.schema import Query, graphql_router

__all__ = [
    "Query",
    "graphql_router",
]
