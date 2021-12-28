import typing as t
from dataclasses import dataclass, field

from .base import Model

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class Bank(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    coins: int = 250


@dataclass()
class Purse(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    coins: int = 50


@dataclass()
class Money(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    bank: Bank = Bank()
    purse: Purse = Purse()
    salary: int = 50
