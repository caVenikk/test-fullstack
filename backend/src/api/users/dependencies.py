from fastapi import Depends

from src.api.users.exceptions import UserNotFound
from src.api.users.models import User
from src.repository.crud import CRUD


async def valid_user_id(user_id: str, crud: CRUD = Depends(CRUD)) -> User:
    if user := await crud.users.get(user_id):
        return user
    raise UserNotFound
