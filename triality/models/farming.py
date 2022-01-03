"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from .base import Model


@dataclass()
class Crop(Model):
    planted_seed: str
    end: datetime
    last_watered: t.Optional[datetime] = None


@dataclass()
class Farm(Model):
    in_progress: t.List[Crop] = field(default_factory=list)
    max_in_progress: int = 10
