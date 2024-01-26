from __future__ import annotations

from typing import Optional

from app import setup


def get_supported_coins(coin_symbol: Optional[str] = None) -> dict | None:
    """
    This function returns a dict that provides further names for the given
    coin needed to send requests to external and to format.


    :param coin_symbol: any of the allowed coin (i.e. btc)
    :return: If coin_symbol is provided
    the response looks like {"id": "bitcoin", "name": "Bitcoin"}
    otherwise it returns all the supported coins
    as defined in the configuration

    {
        "btc": {"id": "bitcoin", "name": "Bitcoin"},
        "xrp": {"id": "ripple", "name": "XRP"},
        "eth": {"id": "ethereum", "name": "Ethereum"},
    }
    """
    coins = setup.supported_coins

    if coin_symbol:
        return coins.get(coin_symbol, None)
    else:
        return coins


def validate_coin(coin_symbol: str) -> dict | None:
    """
    This function checks if the coin_symbol
    is allowed
    :param coin_symbol:
    :return: {"id": "bitcoin", "name": "Bitcoin"} or None
    """
    return get_supported_coins(coin_symbol=coin_symbol.lower())


def validate_amount(amount: int) -> bool:
    """
    This function checks if the  amount
    value is within the allowed range

    :param amount:
    :return:
    """
    return 0 <= amount < setup.max_amount
