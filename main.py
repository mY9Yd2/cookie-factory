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

from typing import Dict


class Warehouse:
    def __init__(self) -> None:
        self.cookies: Dict[str, int] = {"Cookie": 0, "Dark chocolate cookie": 0}

    def list_commodities(self) -> None:
        for cookie_name, quantity in self.cookies.items():
            print(f"\t{cookie_name} : {quantity}")


class Factory:
    def __init__(self, name: str, price: int, production_volume: int) -> None:
        self.quantity: int = 0
        self.name: str = name
        self.price: int = price
        self.production_volume: int = production_volume

    def produce_cookie(self, warehouse: Warehouse) -> None:
        warehouse.cookies["Cookie"] += self.quantity * self.production_volume


class Player:
    def __init__(self, warehouse: Warehouse, factories: Dict[str, Factory]) -> None:
        self.warehouse: Warehouse = warehouse
        self.factories: Dict[str, Factory] = factories

    def buy_factory(self, name: str, quantity: int) -> None:
        if not name in self.factories:
            raise KeyError("There's no such factory!")
        if quantity < 1:
            raise ValueError("The quantity must be a positive number!")

        total_price = quantity * self.factories[name].price

        if self.warehouse.cookies["Cookie"] >= total_price:
            self.factories[name].quantity += quantity
            self.warehouse.cookies["Cookie"] -= total_price
        else:
            raise ValueError("You don't have enough Cookies!")

    def sell_factory(self, name: str, quantity: int) -> None:
        if not name in self.factories:
            raise KeyError("There's no such factory!")
        if quantity < 1:
            raise ValueError("The quantity must be a positive number!")

        if self.factories[name].quantity >= quantity:
            total_price = quantity * self.factories[name].price
            self.warehouse.cookies["Cookie"] += total_price
            self.factories[name].quantity -= quantity
        else:
            raise ValueError("You can't sell more than you have!")

    def list_factories(self) -> None:
        for factory in self.factories.values():
            print(f"\t{factory.name}: {factory.quantity}")

    def create_cookie(self) -> None:
        self.warehouse.cookies["Cookie"] += 1


timer_lock = threading.Lock()


def create_cookie_menu(player: Player) -> None:
    while True:
        match input("\nCookie? "):
            case "cookie":
                with timer_lock:
                    player.create_cookie()
                print("+1 Cookie")
            case "back" | "b":
                break
            case _:
                print("Write 'cookie' or 'back'/'b'")


def warehouse_menu(player: Player) -> None:
    print("\n~Warehouse~")
    with timer_lock:
        player.warehouse.list_commodities()


def factory_menu(player: Player) -> None:
    while True:
        print("\n~Factory~")
        with timer_lock:
            player.list_factories()

        try:
            match input("Choice: ").split():
                case ["buy", name, quantity]:
                    timer_lock.acquire()
                    player.buy_factory(name.capitalize(), int(quantity))
                case ["sell", name, quantity]:
                    timer_lock.acquire()
                    player.sell_factory(name.capitalize(), int(quantity))
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
        except KeyError as error:
            print(error)
        finally:
            if timer_lock.locked():
                timer_lock.release()


def timer(player: Player) -> None:
    with timer_lock:
        for factory in player.factories.values():
            factory.produce_cookie(player.warehouse)

    timer_thread = threading.Timer(1, timer, [player])
    timer_thread.daemon = True
    timer_thread.start()


def main() -> None:
    player = Player(
        Warehouse(),
        {
            "Takodachi": Factory("Takodachi", 5, 1),
            "Robot": Factory("Robot", 25, 10),
            "Farm": Factory("Farm", 500, 10),
            "Mine": Factory("Mine", 5000, 125),
        },
    )

    timer(player)

    while True:
        print(
            "\n~Menu~",
            "1. Warehouse",
            "2. Create cookie",
            "3. Factory",
            "exit - Exit",
            sep="\n\t",
        )

        match input("Choice: "):
            case "exit":
                break
            case "1":
                warehouse_menu(player)
            case "2":
                create_cookie_menu(player)
            case "3":
                factory_menu(player)
            case _:
                print("..?")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
