from app import setup

default_currency = setup.default_currency


def response_template(value: int) -> dict:
    """
    The default response template
    :param value: int

    :return:
    """
    return {default_currency + "_amount": value}
