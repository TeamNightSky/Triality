"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from .base import Model

if t.TYPE_CHECKING:
    from ..core.manager import StorageManager


@dataclass()
class Bid(Model):
    _db: "StorageManager" = field(init=False, repr=False)
    bidder: int
    amount: int
    timestamp: datetime


@dataclass()
class Auction(Model):
    _db: "StorageManager" = field(init=False, repr=False)
    snowflake: int
    item: str
    amount: int
    owner: int
    end: datetime
    start_bid: int = 500
    bids: t.List[Bid] = []
    collected: bool = False
