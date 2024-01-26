import logging
from fastapi import APIRouter
from fastapi import status as http_status
from app.core import http_exceptions
from app import setup
from app.core.api_templates import response_template
from app.exchange.service import Exchange
from app.helpers.coins_validation import validate_amount, validate_coin

logger = logging.getLogger("")
router = APIRouter()
exchange_service = Exchange()


@router.get(
    "",
    status_code=http_status.HTTP_200_OK,
)
async def get_current_price(coin: str, amount: int):
    """
    GET method that return the current price for the given coin
    :param coin:
    :param amount:
    :return:
    :rtype:
    """
    if not validate_amount(amount):
        raise http_exceptions.bad_format()
    if not validate_coin(coin_symbol=coin):
        raise http_exceptions.bad_format()

    response = await exchange_service.exchange(
        crypto_coin_symbol=coin, vs_currency=setup.default_currency, amount=amount
    )
    if response:
        return response_template(value=response)
    else:
        logger.info(f" Unexpected response {response}")
        raise http_exceptions.unprocessable_entity(error="Invalid Amount.")
