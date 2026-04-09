"""Tests für DELETE."""

from typing import Final

from common_test import ctx, login, rest_parkhaeuser_url
from httpx import delete
from pytest import mark


@mark.rest
@mark.delete_request
def test_delete() -> None:
    # arrange
    patient_id: Final = 5

    # act
    response: Final = delete(
        f"{rest_parkhaeuser_url}/{patient_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == 204  # noqa: PLR2004


@mark.rest
@mark.delete_request
def test_delete_not_found() -> None:
    # arrange
    patient_id: Final = 999999

    # act
    response: Final = delete(
        f"{rest_parkhaeuser_url}/{patient_id}",
        verify=ctx,
    )

    # assert
    assert response.status_code == 204  # noqa: PLR2004
