import aiohttp
from typing import Optional, Dict, Any
from app.helpers.requests_utils import handle_exception, trace_session_time
from app.services import crypto_exchange_base_api

client_timeout = aiohttp.ClientTimeout(connect=10)


class CoinGeckoClient:
    """
    This Class provides the current price
    for the given crypto coin
    """

    _base_api_url = crypto_exchange_base_api

    async def get_current_price(
        self, crypto_id: str, vs_currencies: str
    ) -> Dict[str, Any]:
        """
        This method queries the API of coingecko to
        get the current price of the given crypto coin.
        The request sent looks like the following one

        https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd

        and the response looks like
         {"ripple":{"usd":0.637397}}

        :param vs_currencies: the currency, i.e. usd
        :param crypto_id: btc
        :return:


        """
        endpoint = (
            self._base_api_url
            + f"/simple/price?ids={crypto_id}&vs_currencies={vs_currencies}"
        )
        return await self.send_request(method="GET", endpoint=endpoint)

    @staticmethod
    @handle_exception
    async def send_request(
        method: str,
        endpoint: str,
        retry_if_fails: Optional[bool] = False,  # noqa
        **kwargs,  # noqa
    ):
        """
        This method is responsible for sending requests to the provided endpoint
        :param method: one of the supported API methods
        :param endpoint: the endpoint where to send the request
        :param retry_if_fails: yes if you want to retry
        :param kwargs: other parameters
        :return: JSON or None, or it fires a RuntimeError if it gets angry
        """
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

        async with aiohttp.ClientSession(
            trace_configs=[trace_session_time()], timeout=client_timeout
        ) as session:
            raw_response = await session.request(
                url=endpoint, method=method, headers=headers, ssl=False
            )
            status_code = raw_response.status
            if status_code == 404:
                return None
            if status_code == 200:
                return await raw_response.json()
            else:
                raise RuntimeError(f"HTTP Status Error {status_code} from {endpoint}")
