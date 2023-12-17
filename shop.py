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

from player import Player
from factory import Factory
from cookie import Cookie
from effect import PurchasableEffect


class NotEnoughCookie(Exception):
    pass


class NotPositiveNumber(Exception):
    pass


class TooMuchCookie(Exception):
    pass


class NotEnoughFactory(Exception):
    pass


class EffectAlreadyExist(Exception):
    pass


class FactoryShop:
    def __init__(self, player: Player) -> None:
        self._player = player

    @property
    def type_of_currency(self) -> Cookie:
        return Cookie.COOKIE

    def get_price(self, item: Factory) -> int:
        initial_quantity = self._player.factories[item]

        price = self._calculate_total_price(
            initial_quantity=initial_quantity, quantity=1, base_price=item.base_price
        )

        return price

    def _calculate_total_price(
        self, initial_quantity: int, quantity: int, base_price: int
    ) -> int:
        total_price = 0
        for _ in range(quantity):
            try:
                total_price += round(base_price * (1.15**initial_quantity))
            except OverflowError as error:
                raise TooMuchCookie("Too much!") from error
            initial_quantity += 1
        return total_price

    def buy(self, item: Factory, quantity: int) -> int:
        if quantity < 1:
            raise NotPositiveNumber("The quantity must be a positive number!")

        initial_quantity = self._player.factories[item]

        total_price = self._calculate_total_price(
            initial_quantity, quantity, item.base_price
        )

        if total_price > self._player.cookies[self.type_of_currency]:
            message = f"You don't have enough {self.type_of_currency}!"
            message += f"\nIt costs {total_price} {self.type_of_currency}"

            raise NotEnoughCookie(message)

        self._player.cookies[self.type_of_currency] -= total_price
        self._player.factories[item] += quantity

        return total_price

    def sell(self, item: Factory, quantity: int) -> int:
        if quantity < 1:
            raise NotPositiveNumber("The quantity must be a positive number!")

        initial_quantity = self._player.factories[item] - quantity

        if initial_quantity < 0:
            raise NotEnoughFactory("You can't sell more than you have!")

        total_price = self._calculate_total_price(
            initial_quantity, quantity, item.base_price
        )

        self._player.cookies[self.type_of_currency] += total_price
        self._player.factories[item] -= quantity

        return total_price


class EffectShop:
    def __init__(self, player: Player) -> None:
        self._items = {
            PurchasableEffect.LUCK: 50,
        }
        self._player = player

    @property
    def type_of_currency(self) -> Cookie:
        return Cookie.DARK_CHOCOLATE_COOKIE

    @property
    def items(self) -> list[PurchasableEffect]:
        return list(self._items)

    def get_base_price(self, item: PurchasableEffect) -> int:
        return self._items[item]

    def buy(self, item: PurchasableEffect) -> int:
        if item.function in self._player.effects:
            raise EffectAlreadyExist("You already bought this!")

        price = self.get_base_price(item)

        if price > self._player.cookies[self.type_of_currency]:
            message = f"You don't have enough {self.type_of_currency}!"
            message += f"\nIt costs {price} {self.type_of_currency}"

            raise NotEnoughCookie(message)

        self._player.cookies[self.type_of_currency] -= price
        self._player.effects.add(item.function)

        return price
