"""Lasttest mit Locust."""

from typing import Final, Literal

import urllib3
from locust import HttpUser, constant_throughput, task

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GetUser(HttpUser):
    """Lasttest für GET-Requests."""

    wait_time = constant_throughput(0.1)
    MIN_USERS: Final = 500
    MAX_USERS: Final = 500

    def on_start(self) -> None:
        """Start-Skript, um einen JWT im Header für Requests zu speichern."""
        self.client.verify = False

        response: Final = self.client.post(
            url="/auth/token", json={"username": "admin", "password": "p"}
        )
        body: Final[dict[Literal["token"], str]] = response.json()
        token: Final = body["token"]
        self.client.headers = {"Authorization": f"Bearer {token}"}

    @task(100)
    def get_id(self) -> None:
        """GET-Requests mit einer ID als Pfadparameter."""
        for parkhaus_id in [1, 2, 3, 4, 5, 6]:
            response = self.client.get(f"/rest/{parkhaus_id}")
            print(f"{response.json()['id']}")
