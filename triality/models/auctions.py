import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from .base import Model

if t.TYPE_CHECKING:
    from ..core.storage import StorageClient


@dataclass()
class Bid(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    bidder: int
    amount: int
    timestamp: datetime


@dataclass()
class Auction(Model):
    _db: "StorageClient" = field(init=False, repr=False)
    snowflake: int
    item: str
    amount: int
    owner: int
    end: datetime
    start_bid: int = 500
    bids: t.List[Bid] = []
    collected: bool = False
