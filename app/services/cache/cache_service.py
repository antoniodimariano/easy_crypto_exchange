from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from app import setup

from app.services.cache.simple_cache.simple_cache import SimpleCache

logger = logging.getLogger("exchange")


class MemoryCache:
    _cache_client = SimpleCache()
    _default_cache_ttl_in_sec = setup.cache_ttl_in_secs or 180

    def store_result(
        self, crypto: str, vs_currency: str, amount: int, result: float
    ) -> bool:
        """
        This method creates a tuple with the provided input and
        use it as the key of the dict where to store the result

        :param crypto:
        :param vs_currency:
        :param amount:
        :param result:
        :return:
        """
        key = (crypto, vs_currency, amount)
        self._cache_client.set(key=str(key), value=result)
        return True

    def fetch_result(
        self,
        crypto_coin: str,
        vs_currency: str,
        amount: int,
        cache_ttl_in_sec: Optional[int] = _default_cache_ttl_in_sec,
    ) -> Dict[str, str] | None:
        """
        This method checks if a value is stored for
        the tuple built with the provided input.
        It also checks the TTL of the stored value and
        delete the key if it exceeds the cache_ttl value

        The cached value looks like
        {'update': 1700150986, 'value': 36110}

        the update is the timestamp when the data was added. It will be checked in this method
        to ensure that the data returned is fresh.

        :param cache_ttl_in_sec: the TTL in secs
        :param crypto_coin:
        :param vs_currency:
        :param amount:
        :return:
        """
        key = (crypto_coin, vs_currency, amount)

        cached = self._cache_client.get(key=str(key))
        if cached is not None:
            updated = cached.get("update", None)
            if updated is None:
                logger.warning(f"Wrong data format in the cache:  {cached}")
                return None
            updated_object = datetime.fromtimestamp(updated) + timedelta(
                seconds=cache_ttl_in_sec
            )
            current = datetime.now()
            if current < updated_object:
                # data is still fresh
                return cached
            else:
                # data has to be removed
                self._cache_client.remove(key=key)
        else:
            return None
