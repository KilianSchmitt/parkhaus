"""Tests für GET (Suche) ohne und mit Query-Parametern."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, rest_parkhaeuser_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
def test_find_all() -> None:
    # arrange

    # act
    response: Final = get(
        rest_parkhaeuser_url,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0


@mark.rest
@mark.get_request
def test_find_by_name() -> None:
    # arrange
    params = {"name": "Parkhaus Aachen"}

    # act
    response: Final = get(
        rest_parkhaeuser_url,
        params=params,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body.get("content")
    assert isinstance(content, list)
    assert len(content) > 0
    for parkhaus in content:
        assert "aachen" in parkhaus.get("name", "").lower()


@mark.rest
@mark.get_request
def test_find_by_name_teilstring() -> None:
    # arrange
    params = {"name": "aachen"}

    # act
    response: Final = get(
        rest_parkhaeuser_url,
        params=params,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    content: Final = response_body.get("content")
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0].get("name") == "Parkhaus Aachen"


@mark.rest
@mark.get_request
def test_find_not_found() -> None:
    # arrange
    params = {"name": "GibtEsNicht_XYZ"}

    # act
    response: Final = get(
        rest_parkhaeuser_url,
        params=params,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_find_with_pagination() -> None:
    # arrange
    params = {"page": "0", "size": "2"}

    # act
    response: Final = get(
        rest_parkhaeuser_url,
        params=params,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    content: Final = response_body.get("content")
    assert isinstance(content, list)
    assert len(content) <= 2

