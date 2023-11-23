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

from enum import Enum
from cookie import Cookie


class FactoryConfig(Enum):
    TAKODACHI = {
        "name": "takodachi",
        "price": 5,
        "production_volume": {Cookie.COOKIE: 1},
    }
    ROBOT = {"name": "robot", "price": 25, "production_volume": {Cookie.COOKIE: 10}}
    FARM = {"name": "farm", "price": 500, "production_volume": {Cookie.COOKIE: 100}}
    MINE = {
        "name": "mine",
        "price": 5000,
        "production_volume": {Cookie.COOKIE: 250, Cookie.DARK_CHOCOLATE_COOKIE: 1},
    }

    @staticmethod
    def get_price(name: str) -> int:
        price = None
        for config in FactoryConfig:
            if config.value.get("name") == name:
                price = config.value.get("price")
                break
        return price

    @staticmethod
    def is_exist(name: str) -> bool:
        is_exist = False
        for config in FactoryConfig:
            if config.value.get("name") == name:
                is_exist = True
                break
        return is_exist


class Factory:
    def __init__(self, factory_config: FactoryConfig) -> None:
        self.quantity: int = 0
        self.name: str = factory_config.value.get("name")
        self.production_volume: dict[Cookie, int] = factory_config.value.get(
            "production_volume"
        )

    def produce_cookies(self) -> dict[Cookie, int]:
        cookies = dict()
        for cookie, volume in self.production_volume.items():
            cookies[cookie] = self.quantity * volume
        return cookies


class FactoryCreator:
    @staticmethod
    def create(factory_config: FactoryConfig) -> Factory:
        return Factory(factory_config)

    @staticmethod
    def create_from_name(name: str) -> Factory:
        _config = None
        for config in FactoryConfig:
            if config.value.get("name") == name:
                _config = config
                break
        return FactoryCreator.create(_config)
