from __future__ import annotations

import logging
from typing import Union
from datetime import datetime
from app.helpers.date_and_time import convert_to_epoc_timestamp

logger = logging.getLogger("simple_cache")


class SimpleCache:
    """
    This Class implements a basic cache to store key:values
    """

    def __init__(self):
        self.cache = {}

    def set(self, key: tuple, value: Union[int, float]):
        """
        This method stores a value inside the cache

        :param key: key where the value will be stored
        :param value: value to be stored
        """
        self.cache[key] = {
            "value": value,
            "update": convert_to_epoc_timestamp(datetime.now()),
        }

    def get(self, key: tuple, default=None) -> dict:
        """
        This method gets a value from the cache

        :param key: key where the value should be present
        :param default: default value to return in case value not present
        :return: value / default value if key not present on cache
        """
        value = self.cache.get(key, default)
        if value:
            logger.info(f"Key {key} found in memory with value {value}")
        else:
            logger.info(f"Key {key} not found in memory")
        return value

    def remove(self, key: tuple, default=None) -> bool:
        """
        this method removes a value from the cache
        :param key: key where the value should be present
        :param default: default value to return in case value not present
        :return: True or False
        """
        value = self.cache.pop(key, default)
        if value:
            logger.info("Cache entry {} removed".format(key))
            return True
        else:
            logger.info("Cache entry {} not found".format(key))
            return False
