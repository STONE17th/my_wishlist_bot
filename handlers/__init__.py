from aiogram import Router
from .commands import command_router
from .inline_handlers import callback_router

main_router = Router()
main_router.include_routers(
    command_router,
    callback_router,
)

__all__ = [
    'main_router',
]
