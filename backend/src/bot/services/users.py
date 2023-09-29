import aiohttp

from src.api.users.schemas import UserBaseSchema, UserPatchSchema, UserSchema
from src.bot.loader import config


async def create_user(user_data: UserBaseSchema) -> UserSchema | None:
    async with aiohttp.ClientSession() as session:
        api_url = f"{config.base_url}/api/users/"
        async with session.post(api_url, json=user_data.model_dump()) as resp:
            if resp.status == 200:
                user = await resp.json()
                return UserSchema(**user)
    return None


async def make_user_admin(user_id: int | None = None, username: str | None = None) -> UserSchema | None:
    if not any((user_id, username)) or all((user_id, username)):
        return None
    async with aiohttp.ClientSession() as session:
        if user_id:
            api_url = f"{config.base_url}/api/users/{user_id}"
        if username:
            api_url = f"{config.base_url}/api/users/by_username/{username}"
        user_patch_data = UserPatchSchema(is_admin=True)
        async with session.patch(api_url, json=user_patch_data.model_dump()) as resp:
            if resp.status == 200:
                user = await resp.json()
                return UserSchema(**user)
    return None


async def is_user_admin(user_id: int | None = None, username: str | None = None) -> bool | None:
    if not any((user_id, username)) or all((user_id, username)):
        return False
    async with aiohttp.ClientSession() as session:
        if user_id:
            api_url = f"{config.base_url}/api/users/{user_id}"
        if username:
            api_url = f"{config.base_url}/api/users/by_username/{username}"
        async with session.get(api_url) as resp:
            if resp.status == 200:
                user = await resp.json()
                return user["is_admin"]
    return False


async def get_admin_ids() -> list[int] | None:
    async with aiohttp.ClientSession() as session:
        api_url = f"{config.base_url}/api/users/admins/"
        async with session.get(api_url) as resp:
            if resp.status == 200:
                admins = await resp.json()
                return [admin["id"] for admin in admins]
    return None
