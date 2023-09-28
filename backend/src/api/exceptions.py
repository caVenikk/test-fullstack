from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class CustomHTTPException(HTTPException):
    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)


class ValidationException(HTTPException):
    def __init__(self, detail: list[dict]):
        super().__init__(HTTP_400_BAD_REQUEST, detail)
