import asyncio
import json
import os
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app import settings
from app.main import app


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        app=app, base_url=f"http://{settings.api_v1_prefix}"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def another_async_client():
    async with AsyncClient(
        app=app, base_url=f"http://{settings.api_v1_prefix}"
    ) as client:
        yield client


@pytest.fixture(scope="function")
def test_data() -> dict:
    path = os.getenv("PYTEST_CURRENT_TEST")
    path = os.path.join(*os.path.split(path)[:-1], "data.json")
    if not os.path.exists(path):
        path = os.path.join("app/tests/data", "data.json")

    with open(path, "r") as file:
        data = json.loads(file.read())

    return data
