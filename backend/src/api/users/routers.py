from fastapi import APIRouter, Depends
from fastapi import Query
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src.api.users.dependencies import valid_user_id, valid_username
from src.api.users.models import User
from src.api.users.schemas import UserSchema, UserPatchSchema, UserBaseSchema, UserPatchBaseSchema
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
    validator = UserValidator(user_data, crud)
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


@router.get(
    "/admins/",
    response_model=list[UserSchema],
    status_code=HTTP_200_OK,
)
async def get_admins(request: Request, crud: CRUD = Depends(CRUD)) -> list[UserSchema]:
    admins = await crud.users.admins()
    return TypeAdapter(list[UserSchema]).validate_python(admins)


@router.get(
    "/{user_id}",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
)
async def get_user(
    request: Request,
    user: User = Depends(valid_user_id),
) -> UserSchema:
    return TypeAdapter(UserSchema).validate_python(user)


@router.get(
    "/by_username/{username}",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
)
async def get_user_by_username(
    request: Request,
    user: User = Depends(valid_username),
) -> UserSchema:
    return TypeAdapter(UserSchema).validate_python(user)


@router.patch(
    "/{user_id}",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
)
async def update_user(
    request: Request,
    user_data: UserPatchSchema,
    user: User = Depends(valid_user_id),
    crud: CRUD = Depends(CRUD),
) -> UserSchema:
    updated_user = User(id=user.id, **user_data.model_dump())
    updated_user = await crud.users.update(user=updated_user)
    return TypeAdapter(UserSchema).validate_python(updated_user)


@router.patch(
    "/by_username/{username}",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
)
async def update_user_by_username(
    request: Request,
    user_data: UserPatchBaseSchema,
    user: User = Depends(valid_username),
    crud: CRUD = Depends(CRUD),
) -> UserSchema:
    updated_user = User(id=user.id, **user_data.model_dump())
    updated_user = await crud.users.update(user=updated_user)
    return TypeAdapter(UserSchema).validate_python(updated_user)
