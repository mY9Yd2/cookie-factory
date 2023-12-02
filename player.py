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

from cookie import Cookie
from factory import FactoryList, SimpleFactory
from effect import Effect


class Player:
    def __init__(self) -> None:
        self.cookies: dict[Cookie, int] = dict()
        self.factories: dict[FactoryList, SimpleFactory] = dict()
        self.effects: set[Effect] = set()

    def add_cookie(self, cookie: Cookie, quantity: int) -> None:
        self.cookies.update({cookie: self.cookies.get(cookie, 0) + quantity})

    def remove_cookie(self, cookie: Cookie, quantity: int) -> None:
        if quantity > self.cookies.get(cookie):
            self.cookies.update({cookie: 0})
        else:
            self.cookies.update({cookie: self.cookies.get(cookie) - quantity})

    def add_factory(self, factory: FactoryList, quantity: int) -> None:
        _factory = self.factories.get(
            factory,
            FactoryList.create(factory),
        )
        _factory.quantity += quantity
        self.factories.update({factory: _factory})

    def remove_factory(self, factory: FactoryList, quantity: int) -> None:
        if quantity > self.factories.get(factory).quantity:
            self.factories.get(factory).quantity = 0
        else:
            self.factories.get(factory).quantity -= quantity
