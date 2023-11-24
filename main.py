#!/usr/bin/env python
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
from factory import FactoryConfig


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


def factory_menu(player: Player) -> None:
    while True:
        print("\n~Factory~")
        with timer_lock:
            for factory in FactoryConfig:
                factory_name: str = factory.value.get("name")
                player_factory = player.factories.get(factory.value.get("name"))
                player_factory_quantity = (
                    0 if player_factory is None else player_factory.quantity
                )
                print(f"\t{factory_name.capitalize()} : {player_factory_quantity}")

        is_acquired = False
        try:
            match input("Choice: ").split():
                case ["buy", name, quantity]:
                    timer_lock.acquire()
                    is_acquired = True

                    quantity = int(quantity)

                    if quantity < 1:
                        raise ValueError("The quantity must be a positive number!")
                    if not FactoryConfig.is_exist(name):
                        raise ValueError("There's no such factory!")

                    total_price = FactoryConfig.get_price(name) * quantity

                    if player.cookies.get(Cookie.COOKIE, 0) < total_price:
                        raise ValueError("You don't have enough Cookies!")

                    player.remove_cookie(Cookie.COOKIE, total_price)
                    player.add_factory(name, quantity)
                case ["sell", name, quantity]:
                    timer_lock.acquire()
                    is_acquired = True

                    quantity = int(quantity)

                    if quantity < 1:
                        raise ValueError("The quantity must be a positive number!")
                    if name not in player.factories:
                        raise ValueError("There's no such factory!")
                    if quantity > player.factories.get(name).quantity:
                        raise ValueError("You can't sell more than you have!")

                    total_price = FactoryConfig.get_price(name) * quantity
                    player.add_cookie(Cookie.COOKIE, total_price)
                    player.remove_factory(name, quantity)
                case ["back"] | ["b"]:
                    break
                case _:
                    print(
                        "Write 'back'/'b' or for example",
                        "\n'buy takodachi 1'",
                        "\n<buy/sell> <factory-name> <quantity>",
                    )
        except ValueError as error:
            if "invalid literal for int() with base 10" in str(error):
                print("The quantity must be a whole number!")
            else:
                print(error)
        finally:
            if timer_lock.locked() and is_acquired:
                timer_lock.release()


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
            "3. Factory",
            "4. I'm lucky",
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
                factory_menu(player)
            case "4":
                luck_menu(player)
            case _:
                print("..?")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
