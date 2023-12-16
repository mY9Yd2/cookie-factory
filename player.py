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

from collections import Counter

from cookie import Cookie
from factory import Factory
from effect import EffectFn


class Player:
    def __init__(self) -> None:
        self._cookies: Counter[Cookie] = Counter()
        self._factories: Counter[Factory] = Counter()
        self._effects: set[EffectFn] = set()

    @property
    def cookies(self) -> Counter[Cookie]:
        return self._cookies

    @cookies.setter
    def cookies(self, value) -> None:
        self._cookies = value

    @property
    def factories(self) -> Counter[Factory]:
        return self._factories

    @property
    def effects(self) -> set[EffectFn]:
        return self._effects
