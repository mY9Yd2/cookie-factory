# MIT License
#
# Copyright (c) 2023 Kovács József Miklós
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import StrEnum, unique, auto
from dataclasses import dataclass

from cookie import Cookie


@unique
class Factory(StrEnum):
    TAKODACHI = auto()
    ROBOT = auto()
    FARM = auto()
    MINE = auto()

    @property
    def production_volume(self) -> dict[Cookie, int]:
        return {
            Factory.TAKODACHI: {Cookie.COOKIE: 1},
            Factory.ROBOT: {Cookie.COOKIE: 8},
            Factory.FARM: {Cookie.COOKIE: 47},
            Factory.MINE: {Cookie.COOKIE: 260, Cookie.DARK_CHOCOLATE_COOKIE: 1},
        }[self]

    @property
    def base_price(self) -> int:
        return {
            Factory.TAKODACHI: 5,
            Factory.ROBOT: 67,
            Factory.FARM: 733,
            Factory.MINE: 8000,
        }[self]

    @property
    def type_of_currency(self) -> Cookie:
        return Cookie.COOKIE

    def __str__(self) -> str:
        return self.value.capitalize()


@dataclass
class FactoryInfo:
    type: Factory
    production_volume: dict[Cookie, int]
