"""Tests für Queries mit GraphQL."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, graphql_url, login_graphql
from httpx import post
from pytest import mark

GRAPHQL_PATH: Final = "/graphql"


@mark.graphql
@mark.query
def test_query_id() -> None:
    # arrange
    query: Final = {
        "query": """
            {
                parkhaus(parkhausId: "1") {
                    id
                    version
                    name
                    kapazitaet
                    tarifProStunde
                    adresse {
                        plz
                        ort
                        strasse
                        hausnummer
                    }
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    data: Final = response_body["data"]
    assert data is not None
    parkhaus: Final = data["parkhaus"]
    assert isinstance(parkhaus, dict)
    assert response_body.get("errors") is None


@mark.graphql
@mark.query
def test_query_id_notfound() -> None:
    # arrange
    query: Final = {
        "query": """
            {
                parkhaus(parkhausId: "999999") {
                    name
                }
            }
        """,
    }

    # act
    response: Final = post(graphql_url, json=query, verify=ctx)

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    assert response_body["data"]["parkhaus"] is None
    assert response_body.get("errors") is None
