#!/usr/bin/env python3
#
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

import sys
import threading
import random

from collections import Counter

from player import (
    Player,
    NotEnoughCookie,
    TooMuchCookie,
    NotPositiveNumber,
    NotEnoughFactory,
    EffectAlreadyExist,
)
from factory import Factory, FactoryInfo
from effect import ObtainableEffect, PurchasableEffect, effect_composition
from cookie import Cookie

timer_lock = threading.Lock()


def buy_factory(player: Player, item: Factory, quantity: int) -> None:
    try:
        total_price = player.buy_factory(item, quantity)
        print(f"-{total_price} {item.type_of_currency}")
        print(f"+{quantity} {item.capitalize()}")
    except (NotEnoughCookie, TooMuchCookie, NotPositiveNumber) as error:
        print(error)


def sell_factory(player: Player, item: Factory, quantity: int) -> None:
    try:
        total_price = player.sell_factory(item, quantity)
        print(f"-{quantity} {item.capitalize()}")
        print(f"+{total_price} {item.type_of_currency}")
    except (NotPositiveNumber, NotEnoughFactory) as error:
        print(error)


def create_cookie_menu(player: Player) -> None:
    while True:
        match input("\nCookie? "):
            case "cookie":
                with timer_lock:
                    player.cookies[Cookie.COOKIE] += 1
                print(f"+1 {Cookie.COOKIE}")
            case "back" | "b":
                break
            case _:
                print("Write 'cookie' or 'back'/'b'")


def cookies_menu(player: Player) -> None:
    print("\n~Cookies~")
    with timer_lock:
        for cookie, quantity in player.cookies.items():
            print(f"\t{cookie} : {quantity}")


def factory_shop_menu(player: Player) -> None:
    def _is_valid(item: str, quantity: str) -> bool:
        is_valid = False
        try:
            item = Factory(item)
            quantity = int(quantity)
            is_valid = True
        except ValueError as error:
            if str(error).endswith("is not a valid Factory"):
                print(error)
            else:
                print("The quantity must be a whole positive number!")
        return is_valid

    while True:
        print("\n~Factory shop~")

        with timer_lock:
            for item in Factory:
                quantity = player.factories.get(item, 0)
                price = Player.get_next_factory_price(
                    player.factories[item], item.base_price
                )
                print(f"\t{item} : {price} ({quantity})")

        match input("Choice: ").split():
            case ["buy", item, quantity]:
                with timer_lock:
                    if _is_valid(item, quantity):
                        buy_factory(player, Factory(item), int(quantity))
            case ["sell", item, quantity]:
                with timer_lock:
                    if _is_valid(item, quantity):
                        sell_factory(player, Factory(item), int(quantity))
            case ["back"] | ["b"]:
                break
            case _:
                print(
                    "Write 'back'/'b' or for example",
                    "\n'buy takodachi 1'",
                    "\n<buy/sell> <factory-name> <quantity>",
                )


def effect_shop_menu(player: Player) -> None:
    while True:
        print("\n~Effect shop~")

        with timer_lock:
            for item in PurchasableEffect:
                status = "+" if item.function in player.effects else item.base_price
                print(f"\t{item} : {status}")

        match input("Choice: ").split():
            case ["buy", name]:
                with timer_lock:
                    try:
                        item = PurchasableEffect(name)
                    except ValueError as error:
                        print(f"'{name}' is not a valid Effect")
                        continue

                    try:
                        price = player.buy_effect(item)
                        print(f"-{price} {item.type_of_currency}")
                        print(f"+{PurchasableEffect(name)}")
                    except (EffectAlreadyExist, NotEnoughCookie) as error:
                        print(error)
            case ["back"] | ["b"]:
                break
            case _:
                print(
                    "Write 'back'/'b' or for example",
                    "\n'buy luck'",
                    "\n<buy> <effect-name>",
                )


def luck_menu(player: Player) -> None:
    print("\n~I'm lucky~")

    effect = random.choices(
        (None, ObtainableEffect.INANIS, ObtainableEffect.DARKNESS),
        weights=(100, 1, 1),
        k=1,
    )[0]

    with timer_lock:
        if effect is None:
            print("No, you are not lucky.")
        elif effect.function in player.effects:
            print("You already have a lot of luck.")
        else:
            print("You're really lucky!")
            if effect == ObtainableEffect.INANIS:
                print("Takodachis are working harder!")
            elif effect == ObtainableEffect.DARKNESS:
                print("Dark chocolate cookies..")
            player.effects.add(effect.function)


def timer(player: Player) -> None:
    """A new thread dealing with the player's factories, which produce cookies every second"""

    with timer_lock:
        produce_cookies = effect_composition(*player.effects)
        for factory, quantity in player.factories.items():
            info = FactoryInfo(factory, factory.production_volume)
            cookies = Counter(produce_cookies(info).production_volume)

            for cookie in cookies.keys():
                cookies[cookie] *= quantity

            player.cookies += cookies

    timer_thread = threading.Timer(1, timer, [player])
    timer_thread.daemon = True
    timer_thread.start()


def main() -> None:
    player = Player()

    timer(player)

    while True:
        print(
            "\n~Menu~",
            "1. Cookies",
            "2. Create cookie",
            "3. Factory shop",
            "4. I'm lucky",
            "5. Effect shop",
            "exit - Exit",
            sep="\n\t",
        )

        match input("Choice: "):
            case "exit":
                break
            case "1":
                cookies_menu(player)
            case "2":
                create_cookie_menu(player)
            case "3":
                factory_shop_menu(player)
            case "4":
                luck_menu(player)
            case "5":
                effect_shop_menu(player)
            case _:
                print("..?")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
