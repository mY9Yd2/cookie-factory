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
    """Contains cookies, factories and effects that the player has"""

    def __init__(self) -> None:
        self.cookies: Counter[Cookie] = Counter()
        self.factories: Counter[Factory] = Counter()
        self.effects: set[EffectFn] = set()

    @staticmethod
    def get_next_factory_price(initial_quantity: int, base_price: int) -> int:
        """Calculate the next factory price deepending on the initial quantity of factory that the player has

        Args:
            initial_quantity: The number of factories the player currently owns
            base_price: The base price of the factory

        Returns:
            The price of the next factory

        Raises:
            TooMuchCookie: An error occurred during the calculation, when the number is so large that the program cannot able to handle
        """

        try:
            return round(base_price * (1.15**initial_quantity))
        except OverflowError as error:
            raise TooMuchCookie("Too much!") from error

    def buy_factory(self, item: Factory, quantity: int) -> int:
        """Add the factory to the player's factories and subtract its price from the player's cookies

        Args:
            item: The factory the player wants to buy
            quantity: The amount of factory the player wants to buy

        Returns:
            The total price paid by the player

        Raises:
            NotPositiveNumber: An error occurred if the quantity is less than one
            NotEnoughCookie: An error occurred when the player didn't have enough cookies to buy the factories
        """

        if quantity < 1:
            raise NotPositiveNumber("The quantity must be a positive number!")

        total_price = 0
        for q in range(quantity):
            initial_quantity = self.factories[item] + q
            total_price += Player.get_next_factory_price(
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
        """Remove the factory from the player's factories and add its price to the player's cookies

        Args:
            item: The factory the player wishes to sell
            quantity: The amount of factory the player wishes to sell

        Returns:
            The total price that the player has received for the factory

        Raises:
            NotPositiveNumber: An error occurred if the quantity is less than one
            NotEnoughFactory: An error occurred when the player didn't have enough factories that the player want to sell
        """

        if quantity < 1:
            raise NotPositiveNumber("The quantity must be a positive number!")

        if self.factories[item] - quantity < 0:
            raise NotEnoughFactory("You can't sell more than you have!")

        total_price = 0
        for q in range(quantity):
            initial_quantity = self.factories[item] - quantity + q
            total_price += Player.get_next_factory_price(
                initial_quantity, item.base_price
            )

        self.cookies[item.type_of_currency] += total_price
        self.factories[item] -= quantity

        return total_price

    def buy_effect(self, item: PurchasableEffect) -> int:
        """Add the effect to the player's effects and subtract its price from the player's cookies

        Args:
            item: The effect the player wants to buy

        Returns:
            The total price paid by the player

        Raises:
            EffectAlreadyExist: An error occurred if the effect is already exists in the player's effects
            NotEnoughCookie: An error occurred when the player didn't have enough cookies to buy the effect
        """

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
