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

import effect

from player import Player
from cookie import Cookie

from factory import FactoryList
from shop import FactoryShop, EffectShop

timer_lock = threading.Lock()


def create_cookie_menu(player: Player) -> None:
    while True:
        match input("\nCookie? "):
            case "cookie":
                with timer_lock:
                    player.add_cookie(Cookie.COOKIE, 1)
                print(f"+1 {Cookie.COOKIE.value.capitalize()}")
            case "back" | "b":
                break
            case _:
                print("Write 'cookie' or 'back'/'b'")


def cookies_menu(player: Player) -> None:
    print("\n~Cookies~")
    with timer_lock:
        for cookie, quantity in player.cookies.items():
            print(f"\t{cookie.value.capitalize()} : {quantity}")


def factory_shop_menu(player: Player) -> None:
    while True:
        print("\n~Factory shop~")
        shop = FactoryShop(player)
        with timer_lock:
            for item in shop.items:
                player_factory = player.factories.get(item)
                player_factory_quantity = (
                    0 if player_factory is None else player_factory.quantity
                )
                print(
                    f"\t{item} : {shop.get_buy_price(item)} ({player_factory_quantity})"
                )

        match input("Choice: ").split():
            case ["buy", name, quantity]:
                with timer_lock:
                    try:
                        quantity = int(quantity)
                        if quantity < 1:
                            raise ValueError
                    except ValueError:
                        print("The quantity must be a whole positive number!")
                        continue

                    try:
                        if FactoryList(name) not in shop.items:
                            raise ValueError
                    except ValueError:
                        print("There's no such factory!")
                        continue

                    try:
                        total_price = shop.get_buy_price(name, quantity)
                    except OverflowError:
                        print("Too much!")
                        continue

                    if player.cookies.get(shop.type_of_currency, 0) < total_price:
                        print(f"You don't have enough {shop.type_of_currency}!")
                        print(f"It costs {total_price} {shop.type_of_currency}")
                        continue

                    player.remove_cookie(shop.type_of_currency, total_price)
                    player.add_factory(FactoryList(name), quantity)
                    print(f"-{total_price} {shop.type_of_currency}")
                    print(f"+{quantity} {FactoryList(name)}")
            case ["sell", name, quantity]:
                with timer_lock:
                    try:
                        quantity = int(quantity)
                        if quantity < 1:
                            raise ValueError
                    except ValueError:
                        print("The quantity must be a whole positive number!")
                        continue

                    try:
                        if FactoryList(name) not in player.factories:
                            raise ValueError
                    except ValueError:
                        print("There's no such factory!")
                        continue

                    if quantity > player.factories.get(FactoryList(name)).quantity:
                        print("You can't sell more than you have!")
                        continue

                    total_price = shop.get_sell_price(name, quantity)
                    player.add_cookie(shop.type_of_currency, total_price)
                    player.remove_factory(FactoryList(name), quantity)
                    print(f"-{quantity} {FactoryList(name)}")
                    print(f"+{total_price} {shop.type_of_currency}")
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
        shop = EffectShop(player)
        with timer_lock:
            for item in shop.items:
                player_effect = (
                    "+" if item.create() in player.effects else shop.get_buy_price(item)
                )
                print(f"\t{item} : {player_effect}")

        match input("Choice: ").split():
            case ["buy", name]:
                with timer_lock:
                    try:
                        _effect = effect.EffectList(name)
                        if _effect not in shop.items:
                            raise ValueError
                    except ValueError:
                        print("There's no such effect!")
                        continue

                    if _effect.create() in player.effects:
                        print("You already bought this")
                        continue

                    price = shop.get_buy_price(name)
                    if player.cookies.get(shop.type_of_currency, 0) < price:
                        print(f"You don't have enough {shop.type_of_currency}!")
                        continue

                    player.remove_cookie(shop.type_of_currency, price)
                    player.effects.add(_effect.create())
                    print(f"-{price} {shop.type_of_currency}")
                    print(f"+{_effect}")
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
    _effect = random.choices(
        (None, effect.Inanis, effect.Darkness), weights=(100, 1, 1), k=1
    )[0]

    with timer_lock:
        if _effect is None:
            print("No, you are not lucky.")
        elif _effect in player.effects:
            print("You already have a lot of luck.")
        else:
            print("You're really lucky!")
            if _effect == effect.Inanis:
                print("Takodachis are working harder!")
            elif _effect == effect.Darkness:
                print("Dark chocolate cookies..")
            player.effects.add(_effect)


def timer(player: Player) -> None:
    with timer_lock:
        for factory in player.factories.values():
            for _effect in player.effects:
                factory = _effect(factory)
            cookies = factory.produce_cookies()
            for cookie, quantity in cookies.items():
                player.add_cookie(cookie, quantity)

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
