"""Modul für den DB-Zugriff."""

from parkhaus.repository.pageable import MAX_PAGE_SIZE, Pageable
from parkhaus.repository.parkhaus_repository import ParkhausRepository
from parkhaus.repository.sesssion_factory import Session, engine
from parkhaus.repository.slice import Slice

# https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
__all__ = [
    "MAX_PAGE_SIZE",
    "Pageable",
    "ParkhausRepository",
    "Session",
    "Slice",
    "engine",
]
