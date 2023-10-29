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


class Player:
    def __init__(self, warehouse) -> None:
        self.warehouse = warehouse

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


def main() -> None:
    player = Player(Warehouse())

    while True:
        print(
            "\n~Menu~",
            "1. Warehouse",
            "2. Create cookie",
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
            case _:
                print("..?")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
