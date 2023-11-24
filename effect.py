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

from factory import Factory, FactoryConfig
from cookie import Cookie


class Effect(Factory):
    _factory: Factory = None

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
        multiplier = 1
        if self.name == FactoryConfig.TAKODACHI.value.get("name"):
            multiplier = 2
        new_value = cookies.get(Cookie.COOKIE, 0) * multiplier
        cookies.update({Cookie.COOKIE: new_value})
        return cookies


class Darkness(Effect):
    def produce_cookies(self) -> dict[Cookie, int]:
        cookies = self.factory.produce_cookies()
        new_value = cookies.get(Cookie.DARK_CHOCOLATE_COOKIE, 0) * 2
        cookies.update({Cookie.DARK_CHOCOLATE_COOKIE: new_value})
        return cookies
