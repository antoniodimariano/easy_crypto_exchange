import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
DEFAULT_RETRY_DELAY_IN_SECS = 5


async def on_request_start(
    session, trace_config_ctx, params
):  # noqa # pragma: no cover
    trace_config_ctx.start = asyncio.get_event_loop().time()


async def on_request_end(session, trace_config_ctx, params):  # noqa # pragma: no cover
    elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
    logger.info("Request took {} seconds".format(elapsed))


def trace_session_time():  # pragma: no cover
    """
    This function gets response time and response size
    while using aiohttp

    :return:
    """
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    return trace_config


def handle_exception(func):
    """
    This decorator handles the following exception that might occur
    during an aiohttp request

    - TimeoutError : if the `retry_if_fails` kwarg is defined, the request is retried after a delay
    - ClientConnectorError
    - ClientResponseError
    - general Exception : it's also raised when the maximum number of retry attempts is reached

    :param func:
    :return:
    """

    async def wrapper(*args, **kwargs):  # pragma: no cover
        request_counter = kwargs.get("request_counter", 0)
        try:
            kwargs.pop("request_counter", {})
            if request_counter > 10:
                raise Exception(
                    f"Maximum number of attempts to {kwargs.get('method')} {kwargs.get('endpoint')} reached."
                )  # noqa
            return await func(*args, **kwargs)

        except asyncio.TimeoutError:
            if kwargs.get("retry_if_fails", 0):
                logger.warning(
                    f"Request to {kwargs.get('method')} {kwargs.get('endpoint')} timeout. Retrying in "
                    f"{DEFAULT_RETRY_DELAY_IN_SECS} secs"
                )
                await asyncio.sleep(DEFAULT_RETRY_DELAY_IN_SECS)
                kwargs["request_counter"] = request_counter + 1
                return await func(*args, **kwargs)
            else:
                logger.error(
                    f"Request timeout!  {kwargs.get('method')} {kwargs.get('endpoint')}"
                )
        except aiohttp.client.ClientConnectorError:
            logger.error(
                f"A CONNECTION ERROR OCCURRED. CHECK THE URL {kwargs.get('endpoint')}"
            )
        except aiohttp.client.ClientResponseError:
            logger.error(f"Client Response Error from {kwargs.get('endpoint')}")
        except asyncio.exceptions.CancelledError:
            if kwargs.get("retry_if_fails", 0):
                logger.warning(
                    f"Request to {kwargs.get('method')} {kwargs.get('endpoint')} timeout. Retrying in "
                    f"{DEFAULT_RETRY_DELAY_IN_SECS} secs "
                )
                await asyncio.sleep(DEFAULT_RETRY_DELAY_IN_SECS)
                kwargs["request_counter"] = request_counter + 1
                return await func(*args, **kwargs)

        except Exception as error:
            msg = f"Error {error} from {kwargs.get('endpoint')}"
            raise RuntimeError(msg)

    return wrapper
