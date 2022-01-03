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
class Pet(Model):
    _db: "StorageManager" = field(init=False, repr=False)
    display_name: str
    type_id: int
    svg_id: int
    color: t.Tuple[int]

    # last_fed?


@dataclass()
class PetHouse(Model):
    _db: "StorageManager" = field(init=False, repr=False)
    pets: t.List[Pet] = field(default_factory=list)
    max_pets: int = 3
