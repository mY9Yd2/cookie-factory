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

import random
import copy

from functools import reduce
from typing import Callable
from enum import StrEnum, auto, unique

from factory import Factory, FactoryInfo
from cookie import Cookie


EffectFn = Callable[[FactoryInfo], FactoryInfo]


def effect_composition(*func: EffectFn) -> EffectFn:
    """Combine the effect functions into one"""

    def compose(f: EffectFn, g: EffectFn) -> EffectFn:
        return lambda x: f(g(x))

    return reduce(compose, func, lambda x: x)


def inanis(factory: FactoryInfo) -> FactoryInfo:
    """Make the Takodachi factory to produce twice as many cookies"""

    _factory = copy.deepcopy(factory)
    if _factory.type is Factory.TAKODACHI:
        _factory.production_volume[Cookie.COOKIE] *= 2
    return _factory


def darkness(factory: FactoryInfo) -> FactoryInfo:
    """Doubles the amount of Dark chocolate cookie produced by the factory"""

    _factory = copy.deepcopy(factory)
    if Cookie.DARK_CHOCOLATE_COOKIE in _factory.production_volume:
        _factory.production_volume[Cookie.DARK_CHOCOLATE_COOKIE] *= 2
    return _factory


def luck(factory: FactoryInfo) -> FactoryInfo:
    """Chance to add five of every cookie the factory produces"""

    _factory = copy.deepcopy(factory)
    if random.choices((True, False), weights=[1, 50], k=1)[0]:
        for cookie in _factory.production_volume.keys():
            _factory.production_volume[cookie] += 5
    return _factory


@unique
class PurchasableEffect(StrEnum):
    """Effects that the player can buy"""

    LUCK = auto()

    @property
    def function(self) -> EffectFn:
        """Returns the corresponding effect function"""

        return {
            PurchasableEffect.LUCK: luck,
        }[self]

    @property
    def base_price(self) -> int:
        """Returns the price of the effect"""

        return {
            PurchasableEffect.LUCK: 50,
        }[self]

    @property
    def type_of_currency(self) -> Cookie:
        """Returns the type of currency"""

        return Cookie.DARK_CHOCOLATE_COOKIE

    def __str__(self) -> str:
        return self.value.capitalize()


@unique
class ObtainableEffect(StrEnum):
    """Effects that the player can obtain from various game mechanics"""

    INANIS = auto()
    DARKNESS = auto()

    @property
    def function(self) -> EffectFn:
        """Returns the corresponding effect function"""

        return {
            ObtainableEffect.INANIS: inanis,
            ObtainableEffect.DARKNESS: darkness,
        }[self]

    def __str__(self) -> str:
        return self.name.capitalize()
