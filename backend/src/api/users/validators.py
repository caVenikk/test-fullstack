from src.api.exceptions import ValidationException
from src.api.users.schemas import UserBaseSchema, UserPatchSchema
from src.repository.crud import CRUD


class UserValidator:
    def __init__(self, user: UserBaseSchema | UserPatchSchema, crud: CRUD):
        self.user = user
        self.crud = crud
        self._errors: list[dict] = []

    async def validate(self) -> None:
        await self.validate_username_is_unique()

        if self._errors:
            raise ValidationException(self._errors)

    async def validate_username_is_unique(self) -> None:
        if self.user.username is not None and self.user.username in [u.username for u in (await self.crud.users.all())]:
            self._errors.append({"error": "User with username already exists"})
