import pytest
from unittest.mock import patch
from httpx import AsyncClient
from app.tests.utils.strings_util import generate_all_possible_combination


@pytest.mark.asyncio
@patch(
    "app.services.crypto_exchange.coin_gecko.CoinGeckoClient.send_request",
    return_value=None,
)
async def test_unprocessable_response(
    async_client: AsyncClient, another_async_client: AsyncClient, test_data: dict
):
    response = await another_async_client.get("/exchange?coin=btc&amount=10")
    received_response = response.json()
    assert response.status_code == 422
    expected_response = test_data["api_messages"]["bad_amount"]
    assert received_response == expected_response


@pytest.mark.asyncio
@patch(
    "app.services.crypto_exchange.coin_gecko.CoinGeckoClient.send_request",
    return_value={"bitcoin": {"usd": 37488}},
)
async def test_get_price_btc(
    async_client: AsyncClient, another_async_client: AsyncClient, test_data: dict
):
    all_values_to_test = generate_all_possible_combination(string_to_change="btc")
    for coin in all_values_to_test:
        response = await another_async_client.get(f"/exchange?coin={coin}&amount=10")
        received_response = response.json()
        assert response.status_code == 200

        expected_response = test_data["coins"]["btc"]["our_service"]
        assert received_response == expected_response


@pytest.mark.asyncio
@patch(
    "app.services.crypto_exchange.coin_gecko.CoinGeckoClient.send_request",
    return_value={"ripple": {"usd": 0.645209}},
)
async def test_get_price_rpx(
    async_client: AsyncClient, another_async_client: AsyncClient, test_data: dict
):
    all_values_to_test = generate_all_possible_combination(string_to_change="xrp")
    for coin in all_values_to_test:
        response = await another_async_client.get(f"/exchange?coin={coin}&amount=10")
        received_response = response.json()
        assert response.status_code == 200

        expected_response = test_data["coins"]["xrp"]["our_service"]
        assert received_response == expected_response


@pytest.mark.asyncio
@patch(
    "app.services.crypto_exchange.coin_gecko.CoinGeckoClient.send_request",
    return_value={"ethereum": {"usd": 2065.55}},
)
async def test_get_price_eth(
    async_client: AsyncClient, another_async_client: AsyncClient, test_data: dict
):
    all_values_to_test = generate_all_possible_combination(string_to_change="eth")
    for coin in all_values_to_test:
        response = await another_async_client.get(f"/exchange?coin={coin}&amount=10")
        received_response = response.json()
        assert response.status_code == 200

        expected_response = test_data["coins"]["eth"]["our_service"]
        assert received_response == expected_response


@pytest.mark.asyncio
async def test_bad_amount(
    async_client: AsyncClient, another_async_client: AsyncClient, test_data: dict
):
    response = await another_async_client.get("/exchange?coin=btc&amount=-1")
    received_response = response.json()
    assert response.status_code == 400
    expected_response = test_data["api_messages"]["bad_amount"]
    assert received_response == expected_response

    response = await another_async_client.get("/exchange?coin=btc&amount=20000000000")
    received_response = response.json()
    assert response.status_code == 400
    expected_response = test_data["api_messages"]["bad_amount"]
    assert received_response == expected_response


@pytest.mark.asyncio
async def test_bad_coin(
    async_client: AsyncClient, another_async_client: AsyncClient, test_data: dict
):
    response = await another_async_client.get("/exchange?coin=ABC&amount=10")
    received_response = response.json()
    assert response.status_code == 400
    expected_response = test_data["api_messages"]["bad_amount"]
    assert received_response == expected_response
    response = await another_async_client.get("/exchange?coin=ABC&amount='")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_bad_coin_and_bad_amount(
    async_client: AsyncClient, another_async_client: AsyncClient, test_data: dict
):
    response = await another_async_client.get("/exchange?coin=ABC&amount=-10")
    received_response = response.json()
    assert response.status_code == 400
    expected_response = test_data["api_messages"]["bad_amount"]
    assert received_response == expected_response
    response = await another_async_client.get("/exchange?coin=&amount=-10")
    received_response = response.json()
    assert response.status_code == 400
    expected_response = test_data["api_messages"]["bad_amount"]
    assert received_response == expected_response
