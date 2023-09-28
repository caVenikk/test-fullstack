from fastapi import APIRouter, Depends
from fastapi import Query
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src.api.users.dependencies import valid_user_id
from src.api.users.models import User
from src.api.users.schemas import UserSchema, UserPatchSchema, UserBaseSchema
from src.api.users.validators import UserValidator
from src.repository.crud import CRUD

router = APIRouter()


@router.post(
    "/",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
)
async def create_user(
    request: Request,
    user_data: UserBaseSchema,
    crud: CRUD = Depends(CRUD),
) -> UserSchema:
    validator = UserValidator(user_data)
    await validator.validate()

    user = User(**user_data.model_dump())

    await crud.users.create(user=user)
    return TypeAdapter(UserSchema).validate_python(user)


@router.get(
    "/",
    response_model=list[UserSchema],
    status_code=HTTP_200_OK,
)
async def get_users(request: Request, crud: CRUD = Depends(CRUD)) -> list[UserSchema]:
    users = await crud.users.all()
    return TypeAdapter(list[UserSchema]).validate_python(users)


@router.patch(
    "/",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
)
async def update_user(
    request: Request,
    user_data: UserPatchSchema,
    user_id: str = Query(),
    crud: CRUD = Depends(CRUD),
) -> UserSchema:
    validator = UserValidator(user_data, crud)
    await validator.validate()

    user = await valid_user_id(user_id)

    updated_user = User(id=user.id, **user_data.model_dump())
    updated_user = await crud.users.update(user=updated_user)
    return TypeAdapter(UserSchema).validate_python(updated_user)
