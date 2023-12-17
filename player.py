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

from collections import Counter

from cookie import Cookie
from factory import Factory
from effect import EffectFn, PurchasableEffect


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


class Player:
    def __init__(self) -> None:
        self.cookies: Counter[Cookie] = Counter()
        self.factories: Counter[Factory] = Counter()
        self.effects: set[EffectFn] = set()

    def get_next_factory_price(self, initial_quantity: int, base_price: int) -> int:
        try:
            return round(base_price * (1.15**initial_quantity))
        except OverflowError as error:
            raise TooMuchCookie("Too much!") from error

    def buy_factory(self, item: Factory, quantity: int) -> int:
        if quantity < 1:
            raise NotPositiveNumber("The quantity must be a positive number!")

        total_price = 0
        for q in range(quantity):
            initial_quantity = self.factories[item] + q
            total_price += self.get_next_factory_price(
                initial_quantity, item.base_price
            )

        if total_price > self.cookies[item.type_of_currency]:
            message = f"You don't have enough {item.type_of_currency}!"
            message += f"\nIt costs {total_price} {item.type_of_currency}"

            raise NotEnoughCookie(message)

        self.cookies[item.type_of_currency] -= total_price
        self.factories[item] += quantity

        return total_price

    def sell_factory(self, item: Factory, quantity: int) -> int:
        if quantity < 1:
            raise NotPositiveNumber("The quantity must be a positive number!")

        if self.factories[item] - quantity < 0:
            raise NotEnoughFactory("You can't sell more than you have!")

        total_price = 0
        for q in range(quantity):
            initial_quantity = self.factories[item] - quantity + q
            total_price += self.get_next_factory_price(
                initial_quantity, item.base_price
            )

        self.cookies[item.type_of_currency] += total_price
        self.factories[item] -= quantity

        return total_price

    def buy_effect(self, item: PurchasableEffect) -> int:
        if item.function in self.effects:
            raise EffectAlreadyExist("You already bought this!")

        price = item.base_price

        if price > self.cookies[item.type_of_currency]:
            message = f"You don't have enough {item.type_of_currency}!"
            message += f"\nIt costs {price} {item.type_of_currency}"

            raise NotEnoughCookie(message)

        self.cookies[item.type_of_currency] -= price
        self.effects.add(item.function)

        return price
