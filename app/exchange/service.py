from __future__ import annotations

import logging

from app.services.cache.cache_service import MemoryCache
from app.services.crypto_exchange.coin_gecko import CoinGeckoClient
from app.helpers.coins_validation import validate_coin

logger = logging.getLogger("exchange")


def extract_coin_price(
    crypto_coin_symbol: str, response_dict: dict, vs_currency: str
) -> int:
    """
    This function extract the price from the given response and return it.
    :param crypto_coin_symbol: the crypto coin
    :param response_dict: a dict like {'bitcoin': {'usd': 37488}}
    :param vs_currency: the currency the crypto coin is converted into
    :return: an int
    """
    return response_dict.get(
        validate_coin(coin_symbol=crypto_coin_symbol).get("id", None), {}
    ).get(vs_currency)


class BaseExchange:
    """
    This Base Class is responsible for
    fetching the current price of the given crypto coin from an external service.
    Also, a  cache limits the number of requests sent.

    If the request is not found in the cache, it's stored to be used later
    Otherwise, the cached value is returned unless the cache is invalidated

    """

    exchange_client = CoinGeckoClient()
    cache_client = MemoryCache()

    async def exchange(
        self, *, crypto_coin_symbol: str, vs_currency: str, amount: int
    ) -> int | None:
        """
        This method is in charge of returning the current price of the given crypto coin.
        It first checks if a value for the provided input is stored in the cache.
        It sends a request to the external service if no value is found.
        If a valid response is returned, the request is stored in the cache,
        and the current price is returned to the caller.


        :param crypto_coin_symbol: any of the allowed coins
        :param vs_currency: the currency to convert the crypto coin to
        :param amount: the amount of money to convert
        :return:
        """
        cached_price = self.cache_client.fetch_result(
            crypto_coin=crypto_coin_symbol, vs_currency=vs_currency, amount=amount
        )
        if cached_price is not None:
            return int(cached_price.get("value") * amount)
        else:
            crypto_coin_id = validate_coin(coin_symbol=crypto_coin_symbol).get(
                "id", None
            )
            exchange_response = await self.exchange_client.get_current_price(
                crypto_id=crypto_coin_id, vs_currencies=vs_currency
            )
            logger.info(
                f"current price {exchange_response}"
            )  # {'bitcoin': {'usd': 37488}}
            if exchange_response:
                unit_price = extract_coin_price(
                    crypto_coin_symbol=crypto_coin_symbol,
                    response_dict=exchange_response,
                    vs_currency=vs_currency,
                )  # 37488
                if unit_price is None:
                    raise TypeError("UNIT PRICE NOT VALID ")
                # here we store the response
                self.cache_client.store_result(
                    crypto=crypto_coin_symbol,
                    vs_currency=vs_currency,
                    amount=amount,
                    result=unit_price,
                )
                return unit_price * amount
            else:
                return None


class Exchange(BaseExchange):
    def __init__(self):
        super(BaseExchange, self).__init__()

    async def exchange(
        self, *, crypto_coin_symbol: str, vs_currency: str, amount: int
    ) -> int | None:
        exchanged_coins = await super(Exchange, self).exchange(
            crypto_coin_symbol=crypto_coin_symbol,
            vs_currency=vs_currency,
            amount=amount,
        )
        return exchanged_coins
