"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import typing as t
from dataclasses import dataclass, field

from .base import Model

if t.TYPE_CHECKING:
    from ..core.manager import StorageManager


@dataclass()
class XPTable(Model):
    _db: "StorageManager" = field(init=False, repr=False)
    journeying: int = 0
    magical: int = 0
    alchemy: int = 0
    combat: int = 0
    finding: int = 0
    crafting: int = 0
    auctioning: int = 0
    intelligence: int = 0
    farming: int = 0
