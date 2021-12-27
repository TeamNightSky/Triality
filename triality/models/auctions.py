import typing as t
from dataclasses import dataclass
from datetime import datetime

from .base import Model


@dataclass()
class Bid(Model):
    bidder: int
    amount: int
    timestamp: datetime


@dataclass()
class Auction(Model):
    snowflake: int
    item: str
    amount: int
    owner: int
    end: datetime
    start_bid: int = 500
    bids: t.List[Bid] = []
    collected: bool = False
