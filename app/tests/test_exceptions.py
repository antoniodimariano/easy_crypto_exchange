import pytest

from app.core.http_exceptions import bad_format, unprocessable_entity
from fastapi import HTTPException


def test_bad_format_exception():
    with pytest.raises(HTTPException):
        raise bad_format()
    with pytest.raises(HTTPException):
        raise bad_format(error="custom error")


def test_unprocessable_entity_exception():
    with pytest.raises(HTTPException):
        raise unprocessable_entity()
    with pytest.raises(HTTPException):
        raise unprocessable_entity(error="custom error")
