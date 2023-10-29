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


class Warehouse:
    def __init__(self) -> None:
        self.cookies = {"Cookie": 0, "Dark chocolate cookie": 0}

    def list_commodities(self) -> None:
        print()
        for k, v in self.cookies.items():
            print(f"{k} : {v}")


class Factory:
    def __init__(self, name, price, production_volume) -> None:
        self.quantity = 0
        self.name = name
        self.price = price
        self.production_volume = production_volume

    def produceCookie(self, warehouse: Warehouse) -> None:
        warehouse.cookies["Cookie"] += self.quantity * self.production_volume


class Player:
    def __init__(self, warehouse, factories) -> None:
        self.warehouse = warehouse
        self.factories = factories

    def buy_factory(self, name, quantity) -> None:
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

    def sell_factory(self, name, quantity) -> None:
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
        while True:
            match input("Cookie? "):
                case "cookie":
                    self.warehouse.cookies["Cookie"] += 1
                    print("+1 Cookie")
                case "back" | "b":
                    break
                case _:
                    print("Write 'cookie' or 'back'/'b'")


def factory_menu(player: Player):
    while True:
        print("\n~Factory~")
        player.list_factories()

        try:
            match input("Choice: ").split():
                case ["buy", name, quantity]:
                    player.buy_factory(name.capitalize(), int(quantity))
                case ["sell", name, quantity]:
                    player.sell_factory(name.capitalize(), int(quantity))
                case ["back"] | ["b"]:
                    break
                case _:
                    print(
                        "Write 'back'/'b' or for example",
                        "\n'buy takodachi 1'",
                        "\n<buy/sell> <factory-name> <quantity>",
                    )
        except ValueError as e:
            if "invalid literal for int() with base 10" in str(e):
                print("The quantity must be a whole number!")
            else:
                print(e)
        except KeyError as e:
            print(e)


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
                player.warehouse.list_commodities()
            case "2":
                player.create_cookie()
            case "3":
                factory_menu(player)
            case _:
                print("..?")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
