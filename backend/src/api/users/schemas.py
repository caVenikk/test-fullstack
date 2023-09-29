from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]

    class Config:
        from_attributes = True


class UserPatchBaseSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    is_admin: bool | None = None

    class Config:
        from_attributes = True


class UserPatchSchema(UserPatchBaseSchema):
    username: str | None = None


class UserSchema(UserBaseSchema):
    is_admin: bool
