"""Tests für PUT."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, login, rest_parkhaeuser_url
from httpx import put
from pytest import mark


@mark.rest
@mark.put_request
def test_put() -> None:
    # arrange
    parkhaus_id: Final = 1
    if_match: Final = '"0"'
    geaendertes_parkhaus: Final = {
        "name": "Parkhaus am Schloss",
        "kapazitaet": 250,
        "tarif_pro_stunde": "15.00"
    }
    headers = {
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.text


@mark.rest
@mark.put_request
def test_put_invalid() -> None:
    # arrange
    parkhaus_id: Final = 2
    geaendertes_parkhaus_invalid: Final = {
        "name": "Parkhaus am Schloss",
        "kapazitaet": 250,
    }
    headers = {
        "If-Match": '"0"',
    }

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "name" in response.text
    assert "kapazitaet" in response.text
    assert "tarif_pro_stunde" in response.text


@mark.rest
@mark.put_request
def test_put_nicht_vorhanden() -> None:
    # arrange
    parkhaus_id: Final = 999999
    if_match: Final = '"0"'
    geaendertes_parkhaus: Final = {
        "name": "Parkhaus am Schloss",
        "kapazitaet": 250,
        "tarif_pro_stunde": "15.00"
    }
    headers = {
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.put_request
def test_put_ohne_versionsnr() -> None:
    # arrange
    parkhaus_id: Final = 3
    geaendertes_parkhaus: Final = {
        "name": "Parkhaus am Schloss",
        "kapazitaet": 250,
        "tarif_pro_stunde": "15.00"
    }

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus,
        verify=ctx,
    )

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_REQUIRED


@mark.rest
@mark.put_request
def test_put_alte_versionsnr() -> None:
    # arrange
    parkhaus_id: Final = 4
    if_match: Final = '"-1"'
    geaendertes_parkhaus: Final = {
        "name": "Parkhaus am Schloss",
        "kapazitaet": 250,
        "tarif_pro_stunde": "15.00"
    }
    headers = {
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED


@mark.rest
@mark.put_request
def test_put_ungueltige_versionsnr() -> None:
    # arrange
    parkhaus_id: Final = 5
    if_match: Final = '"xy"'
    geaendertes_parkhaus: Final = {
        "name": "Parkhaus am Schloss",
        "kapazitaet": 250,
        "tarif_pro_stunde": "15.00"
    }
    headers = {
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
    assert not response.text


@mark.rest
@mark.put_request
def test_put_versionsnr_ohne_quotes() -> None:
    # arrange
    parkhaus_id: Final = 6
    if_match: Final = "0"
    geaendertes_parkhaus: Final = {
        "name": "Parkhaus am Schloss",
        "kapazitaet": 250,
        "tarif_pro_stunde": "15.00"
    }
    headers = {
        "If-Match": if_match,
    }

    # act
    response: Final = put(
        f"{rest_parkhaeuser_url}/{parkhaus_id}",
        json=geaendertes_parkhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.PRECONDITION_FAILED
