"""Tests für GET mit Pfadparameter für die ID."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
@mark.parametrize("parkhaus_id", [1, 2])
def test_get_by_id(parkhaus_id: int) -> None:
    # arrange

    # act
    response: Final = get(
        f"{rest_url}/{parkhaus_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == parkhaus_id


@mark.rest
@mark.get_request
@mark.parametrize("parkhaus_id", [0, 999999])
def test_get_by_id_not_found(parkhaus_id: int) -> None:
    # arrange

    # act
    response: Final = get(
        f"{rest_url}/{parkhaus_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
def test_get_by_id_parkhaus() -> None:
    # arrange
    parkhaus_id: Final = 1

    # act
    response: Final = get(
        f"{rest_url}/{parkhaus_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    parkhaus_id_response: Final = response_body.get("id")
    assert parkhaus_id_response is not None
    assert parkhaus_id_response == parkhaus_id


@mark.rest
@mark.get_request
@mark.parametrize("parkhaus_id,if_none_match", [(3, '"0"'), (4, '"0"')])
def test_get_by_id_etag(parkhaus_id: int, if_none_match: str) -> None:
    # arrange
    headers = {
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{parkhaus_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_MODIFIED
    assert not response.text


@mark.rest
@mark.get_request
@mark.parametrize("patient_id,if_none_match", [(5, "xxx"), (6, "xxx")])
def test_get_by_id_etag_invalid(patient_id: int, if_none_match: str) -> None:
    # arrange
    headers = {
        "If-None-Match": if_none_match,
    }

    # act
    response: Final = get(
        f"{rest_url}/{patient_id}",
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    response_body: Final = response.json()
    assert isinstance(response_body, dict)
    id_actual: Final = response_body.get("id")
    assert id_actual is not None
    assert id_actual == patient_id
