import asyncio
from aiogram import Dispatcher
from loguru import logger

from src.bot.loader import bot, config, dp
from src.bot.services.users import make_user_admin
from src.bot.handlers.commands import router as commands_router
from src.bot.handlers.product import router as product_router
from src.bot.handlers.user import router as user_router
from src.bot.handlers.callback_query import router as callback_query_router


def on_events():
    async def startup(_: Dispatcher) -> None:
        logger.info("Starting...")
        for user_id in config.telegram.admin_ids:
            await make_user_admin(user_id=user_id)

    async def shutdown(dispatcher: Dispatcher) -> None:
        logger.info("Closing storage...")
        await dispatcher.storage.close()
        logger.info("Bot shutdown...")

    return startup, shutdown


async def main():
    dp.include_router(commands_router)
    dp.include_router(product_router)
    dp.include_router(user_router)
    dp.include_router(callback_query_router)
    logger.info(f"Number of sub_routers: {len(dp.sub_routers)}.")
    logger.info(f"Number of message handlers: {sum(len(router.message.handlers) for router in dp.sub_routers)}.")
    logger.info(
        f"Number of callback query handlers: {sum(len(router.callback_query.handlers) for router in dp.sub_routers)}.",
    )
    on_startup, on_shutdown = on_events()
    await dp.start_polling(
        bot,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )


if __name__ == "__main__":
    asyncio.run(main())
