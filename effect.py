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

import random

from enum import Enum, unique

from factory import Factory, FactoryList
from cookie import Cookie


class Effect(Factory):
    def __init__(self, factory: Factory) -> None:
        self._factory = factory

    @property
    def factory(self) -> Factory:
        return self._factory

    @property
    def name(self) -> str:
        return self._factory.name

    def produce_cookies(self) -> dict[Cookie, int]:
        return self._factory.produce_cookies()


class Inanis(Effect):
    def produce_cookies(self) -> dict[Cookie, int]:
        cookies = self.factory.produce_cookies()
        if FactoryList(self.factory.name) == FactoryList.TAKODACHI:
            cookie = cookies.get(Cookie.COOKIE, 0)
            cookies.update({Cookie.COOKIE: cookie * 2})
        return cookies


class Darkness(Effect):
    def produce_cookies(self) -> dict[Cookie, int]:
        cookies = self.factory.produce_cookies()
        cookie = cookies.get(Cookie.DARK_CHOCOLATE_COOKIE)
        if cookie is not None:
            cookies.update({Cookie.DARK_CHOCOLATE_COOKIE: cookie * 2})
        return cookies


class Luck(Effect):
    def produce_cookies(self) -> dict[Cookie, int]:
        cookies = self.factory.produce_cookies()
        if random.choices((True, False), weights=[1, 50], k=1)[0]:
            for cookie, value in cookies.items():
                cookies.update({cookie: value + 5})
        return cookies


@unique
class EffectList(Enum):
    INANIS = "inanis"
    DARKNESS = "darkness"
    LUCK = "luck"

    def __str__(self) -> str:
        return self.value.capitalize()

    def create(self) -> Effect:
        match self:
            case EffectList.INANIS:
                return Inanis
            case EffectList.DARKNESS:
                return Darkness
            case EffectList.LUCK:
                return Luck
            case _:
                raise ValueError("There's no such effect!")
