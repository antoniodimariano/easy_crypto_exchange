from app.tests.utils.strings_util import generate_all_possible_combination
from app.helpers.coins_validation import validate_coin, get_supported_coins


def test_validate_coins():
    supported_coins_symbols = ["btc", "xrp", "eth"]
    for coin in supported_coins_symbols:
        ret = validate_coin(coin_symbol=coin)
        assert ret is not None
        assert ret.get("id") is not None
        assert ret.get("name") is not None
    ret = validate_coin(coin_symbol="ciaioao")
    assert ret is None

    for coin in supported_coins_symbols:
        values_to_test = generate_all_possible_combination(string_to_change=coin)
        for value in values_to_test:
            ret = validate_coin(coin_symbol=value)
            assert ret is not None
            assert ret.get("id") is not None
            assert ret.get("name") is not None


def test_get_supported_coins():
    ret = get_supported_coins()
    assert ret == {
        "btc": {"id": "bitcoin", "name": "Bitcoin"},
        "xrp": {"id": "ripple", "name": "XRP"},
        "eth": {"id": "ethereum", "name": "Ethereum"},
    }
