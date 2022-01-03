"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

from dataclasses import dataclass

from .base import Model


@dataclass()
class Bank(Model):
    coins: int = 250


@dataclass()
class Purse(Model):
    coins: int = 50


@dataclass()
class Rank(Model):
    level: int = 0
    title: str = "PEASANT"
    salary: int = 50
    image: str = ""
    promotion_chance_increase: float = 0.05
    progress: float = 0


@dataclass()
class Money(Model):
    bank: Bank = Bank()
    purse: Purse = Purse()
    rank: Rank = Rank()
