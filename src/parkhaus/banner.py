"""Banner beim Start des Servers."""

import sys
from collections import namedtuple
from getpass import getuser
from importlib.metadata import version
from locale import getlocale
from socket import gethostbyname, gethostname
from sysconfig import get_platform
from types import FunctionType
from typing import Final

import cryptography
import fastapi
import keycloak
import openpyxl
import psycopg
import pydantic
import sqlalchemy
import starlette
from loguru import logger
from pyfiglet import Figlet
from starlette.routing import BaseRoute, Route
from tabulate import tabulate

from parkhaus.config import db_url

# tabulate() hat ein Argument vom Typ "Tuple" und nicht dataclass
TableEntry = namedtuple("TableEntry", "pfad http_methoden funktion")


def _route_to_table_entry(route: Route) -> TableEntry:
    """Route als Tupel mit Pfad, HTTP-Methode, implementierende Funktion."""
    endpoint: Final = route.endpoint
    qualname: Final = (
        endpoint.__qualname__ if isinstance(endpoint, FunctionType) else "N/A"
    )
    # Liste als String ohne [] und ohne '
    methods_str = str(route.methods)[2:-2] if route.methods is not None else "-"
    # FURB184 wird von ruff (noch) nicht unterstuetzt
    methods_str = methods_str.replace("', '", ", ")
    return TableEntry(
        pfad=route.path,
        http_methoden=methods_str,
        funktion=f"{endpoint.__module__}.{qualname}",
    )


def _routes_to_str(routes: list[BaseRoute]) -> str:
    routes_str: Final = [
        _route_to_table_entry(route) for route in routes if isinstance(route, Route)
    ]
    return tabulate(
        sorted(routes_str),
        headers=["Pfad", "HTTP-Methoden", "Implementierung"],
    )


def banner(routes: list[BaseRoute]) -> None:
    """Banner für den Start des Servers."""
    figlet: Final = Figlet()
    print()
    print(figlet.renderText("parkhaus"))

    rechnername: Final = gethostname()
    # Default Isolation Level "read committed": Schreibsperren und keine Lesesperren
    # https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#transaction-isolation-level
    # https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-ISOLATION

    logger.info("Python           {}", sys.version_info)
    logger.info("Plattform        {}", get_platform())
    logger.info("FastAPI          {}", fastapi.__version__)
    logger.info("uvicorn          {}", version("uvicorn"))
    logger.info("Starlette        {}", starlette.__version__)
    logger.info("AnyIO            {}", version("anyio"))
    logger.info("Pydantic         {}", pydantic.__version__)
    logger.info("Strawberry       {}", version("strawberry-graphql"))
    logger.info("SQLAlchemy       {}", sqlalchemy.__version__)
    logger.info("psycopg          {}", psycopg.__version__)
    logger.info("DB URL           {}", db_url)
    logger.info("python-keycloak  {}", keycloak.__version__)
    logger.info("cryptography     {}", cryptography.__version__)
    logger.info("openpyxl         {}", openpyxl.__version__)
    logger.info("Environment      {}", sys.prefix)
    logger.info("User             {}", getuser())
    logger.info("Locale           {}", getlocale())
    logger.info("Rechnername      {}", rechnername)
    logger.info("IP               {}", gethostbyname(rechnername))
    logger.info("{} Routes:", len(routes))

    print()
    print(_routes_to_str(routes))
    print()
