"""Tests für POST."""

from http import HTTPStatus
from re import search
from typing import Final

from common_test import ctx, rest_parkhaeuser_url
from httpx import post
from pytest import mark


@mark.rest
@mark.post_request
def test_post() -> None:
    # arrange
    neues_parkhaus: Final = {
        "name": "Südpfalz-Parkhaus Bellheim",
        "kapazitaet": 120,
        "tarif_pro_stunde": "2.20",
        "adresse": {
            "plz": "76756",
            "ort": "Bellheim",
            "strasse": "Hauptstraße",
            "hausnummer": "101",
        },
        "autos": [
            {
                "kennzeichen": "GER-JD-2026",
                "einfahrtszeit": "2026-04-02T09:00:00Z",
                "kundentyp": "ANWOHNER",
            }
        ],
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_parkhaeuser_url,
        json=neues_parkhaus,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    location: Final = response.headers.get("Location")
    assert location is not None
    int_pattern: Final = "[1-9][0-9]*$"
    assert search(int_pattern, location) is not None
    assert not response.text


@mark.rest
@mark.post_request
def test_post_invalid() -> None:
    # arrange
    neues_parkhaus_invalid: Final = {
        "name": "Südpfalz-Parkhaus Bellheim",
        "kapazitaet": 120,
        "tarif_pro_stunde": 2.20,
        "adresse": {
            "plz": "76756",
            "ort": "Bellheim",
            "strasse": "Hauptstraße",
            "hausnummer": "101",
        },
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_parkhaeuser_url,
        json=neues_parkhaus_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.text
    assert "tarif_pro_stunde" in body


@mark.rest
@mark.post_request
def test_post_parkhaus_voll() -> None:
    # arrange
    neues_parkhaus_voll: Final = {
        "name": "Südpfalz-Parkhaus Bellheim",
        "kapazitaet": 1,
        "tarif_pro_stunde": "2.20",
        "adresse": {
            "plz": "76756",
            "ort": "Bellheim",
            "strasse": "Hauptstraße",
            "hausnummer": "101",
        },
        "autos": [
            {
                "kennzeichen": "GER-JD-2026",
                "einfahrtszeit": "2026-04-02T09:00:00Z",
                "kundentyp": "ANWOHNER",
            },
            {
                "kennzeichen": "GER-JD-2026",
                "einfahrtszeit": "2026-04-02T09:00:00Z",
                "kundentyp": "ANWOHNER",
            },
        ],
    }
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_parkhaeuser_url,
        json=neues_parkhaus_voll,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Parking Facility is full."


@mark.rest
@mark.post_request
def test_post_invalid_json() -> None:
    # arrange
    json_invalid: Final = '{"name" "parkhaus"}'
    headers = {"Content-Type": "application/json"}

    # act
    response: Final = post(
        rest_parkhaeuser_url,
        content=json_invalid,
        headers=headers,
        verify=ctx,
    )

    # assert
    assert response.status_code in {
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.UNPROCESSABLE_ENTITY,
    }
