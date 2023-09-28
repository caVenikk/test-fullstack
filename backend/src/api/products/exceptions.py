from starlette.status import HTTP_404_NOT_FOUND

from src.api.exceptions import CustomHTTPException


class ProductNotFound(CustomHTTPException):
    status_code = HTTP_404_NOT_FOUND
    detail = "Product not found"
