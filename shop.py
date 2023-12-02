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

from abc import ABC, abstractmethod
from enum import Enum

from factory import FactoryList
from cookie import Cookie


class Shop(ABC):
    @property
    @abstractmethod
    def type_of_currency(self) -> Cookie:
        pass

    @property
    @abstractmethod
    def items(self) -> list[Enum]:
        pass

    @abstractmethod
    def get_price(self, item: str) -> int:
        pass


class FactoryShop(Shop):
    def __init__(self) -> None:
        self._items = {
            FactoryList.TAKODACHI: 5,
            FactoryList.ROBOT: 25,
            FactoryList.FARM: 500,
            FactoryList.MINE: 5000,
        }

    @property
    def type_of_currency(self) -> Cookie:
        return Cookie.COOKIE

    @property
    def items(self) -> list[Enum]:
        return list(self._items)

    def get_price(self, item: str) -> int:
        factory = FactoryList(item)
        return self._items[factory]
