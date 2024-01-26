from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str


class Setup(BaseSettings):
    # Service Setup
    default_currency: str
    supported_coins: dict
    max_amount: int
    crypto_exchange_base_api: str
    cache_ttl_in_secs: int
