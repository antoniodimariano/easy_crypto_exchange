from app.services.cache.cache_service import MemoryCache
from app.services.cache.simple_cache.simple_cache import SimpleCache
import time


def test_memory_test():
    cache = MemoryCache()
    result = cache.store_result(
        crypto="bitcoin", amount=10, vs_currency="usd", result=36110
    )
    assert result is True
    value = cache.fetch_result(crypto_coin="bitcoin", amount=10, vs_currency="usd")
    assert value.get("value") == 36110

    value = cache.fetch_result(crypto_coin="blablal", amount=10, vs_currency="usd")
    assert value is None

    time.sleep(3)
    value = cache.fetch_result(
        crypto_coin="bitcoin", amount=10, vs_currency="usd", cache_ttl_in_sec=2
    )
    assert value is None


def test_simple_cache():
    cache = SimpleCache()
    cache.set(key=("abc", "foo", "bar"), value=1010)
    value = cache.get(key=("abc", "foo", "bar"))
    assert value.get("value") == 1010
    assert isinstance(value, dict)

    value = cache.get(key=("ciao", "foo", "bar"))
    assert value is None
    value = cache.remove(key=("ciaociao", "foo", "bar"))
    assert value is False
    value = cache.remove(key=("abc", "foo", "bar"))
    assert value is True
