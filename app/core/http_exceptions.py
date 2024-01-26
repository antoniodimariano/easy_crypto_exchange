from typing import Optional

from fastapi import HTTPException
from fastapi import status as http_status


def bad_format(error: Optional[str] = None):
    if not error:
        error = "Invalid Amount."
    return HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=error)


def unprocessable_entity(error: Optional[str] = None):  # noqa
    if not error:
        error = "Can't process your data"
    return HTTPException(
        status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error
    )
