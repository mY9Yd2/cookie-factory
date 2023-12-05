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
from enum import Enum, unique

from cookie import Cookie


class Factory(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def produce_cookies(self) -> dict[Cookie, int]:
        pass


class ExtendedFactory(Factory):
    @property
    @abstractmethod
    def quantity(self) -> int:
        pass

    @quantity.setter
    @abstractmethod
    def quantity(self, value) -> None:
        pass

    @property
    @abstractmethod
    def production_volume(self) -> dict[Cookie, int]:
        pass


class SimpleFactory(ExtendedFactory):
    def __init__(self) -> None:
        self._quantity: int = 0

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = value

    def produce_cookies(self) -> dict[Cookie, int]:
        cookies = dict()
        for cookie, volume in self.production_volume.items():
            cookies[cookie] = self.quantity * volume
        return cookies


class Takodachi(SimpleFactory):
    @property
    def name(self) -> str:
        return FactoryList.TAKODACHI.value

    @property
    def production_volume(self) -> dict[Cookie, int]:
        return {Cookie.COOKIE: 1}


class Robot(SimpleFactory):
    @property
    def name(self) -> str:
        return FactoryList.ROBOT.value

    @property
    def production_volume(self) -> dict[Cookie, int]:
        return {Cookie.COOKIE: 8}


class Farm(SimpleFactory):
    @property
    def name(self) -> str:
        return FactoryList.FARM.value

    @property
    def production_volume(self) -> dict[Cookie, int]:
        return {Cookie.COOKIE: 47}


class Mine(SimpleFactory):
    @property
    def name(self) -> str:
        return FactoryList.MINE.value

    @property
    def production_volume(self) -> dict[Cookie, int]:
        return {Cookie.COOKIE: 260, Cookie.DARK_CHOCOLATE_COOKIE: 1}


@unique
class FactoryList(Enum):
    TAKODACHI = "takodachi"
    ROBOT = "robot"
    FARM = "farm"
    MINE = "mine"

    def __str__(self) -> str:
        return self.value.capitalize()

    def create(self) -> ExtendedFactory:
        match self:
            case FactoryList.TAKODACHI:
                return Takodachi()
            case FactoryList.ROBOT:
                return Robot()
            case FactoryList.FARM:
                return Farm()
            case FactoryList.MINE:
                return Mine()
            case _:
                raise ValueError("There's no such factory!")
