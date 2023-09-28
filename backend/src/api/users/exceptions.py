from starlette.status import HTTP_404_NOT_FOUND

from src.api.exceptions import CustomHTTPException


class UserNotFound(CustomHTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = "User not found"
