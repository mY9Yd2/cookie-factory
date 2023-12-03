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

from abc import ABC, abstractmethod
from enum import Enum

from player import Player
from factory import FactoryList
from effect import EffectList
from cookie import Cookie


class Shop(ABC):
    def __init__(self, player: Player) -> None:
        self._player = player

    @property
    @abstractmethod
    def type_of_currency(self) -> Cookie:
        pass

    @property
    @abstractmethod
    def items(self) -> list[Enum]:
        pass

    @abstractmethod
    def get_buy_price(self, item: str, quantity: int = 1) -> int:
        pass


class ShopWithSellOption(Shop):
    @abstractmethod
    def get_sell_price(self, item: str, quantity: int = 1) -> int:
        pass


class FactoryShop(ShopWithSellOption):
    def __init__(self, player: Player) -> None:
        self._items = {
            FactoryList.TAKODACHI: 5,
            FactoryList.ROBOT: 67,
            FactoryList.FARM: 733,
            FactoryList.MINE: 8000,
        }
        super().__init__(player)

    @property
    def type_of_currency(self) -> Cookie:
        return Cookie.COOKIE

    @property
    def items(self) -> list[Enum]:
        return list(self._items)

    def get_buy_price(self, item: str, quantity: int = 1) -> int:
        factory = FactoryList(item)
        base_cost = self._items[factory]

        player_factory = self._player.factories.get(factory)
        player_quantity = 0 if player_factory is None else player_factory.quantity

        total_price = 0
        for _ in range(quantity):
            total_price += round(base_cost * (1.15**player_quantity))
            player_quantity += 1

        return total_price

    def get_sell_price(self, item: str, quantity: int = 1) -> int:
        factory = FactoryList(item)
        base_cost = self._items[factory]

        player_factory = self._player.factories.get(factory)
        player_quantity = 0 if player_factory is None else player_factory.quantity

        total_price = 0
        player_quantity -= quantity
        for _ in range(quantity):
            total_price += round(base_cost * (1.15**player_quantity))
            player_quantity += 1

        return total_price


class EffectShop(Shop):
    def __init__(self, player: Player) -> None:
        self._items = {EffectList.LUCK: 50}
        super().__init__(player)

    @property
    def type_of_currency(self) -> Cookie:
        return Cookie.DARK_CHOCOLATE_COOKIE

    @property
    def items(self) -> list[Enum]:
        return list(self._items)

    def get_buy_price(self, item: str, quantity: int = 1) -> int:
        effect = EffectList(item)
        return self._items[effect]
