from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject, bot: Bot):
    command_split = command.text.split(maxsplit=1)
    if len(command_split) == 1:
        referral_link = f'https://t.me/stone_wishlist_bot?start={message.from_user.id}'
        message_text = f'Здравствуй, хозяин!\nВот твоя реферральная ссылка:\n{referral_link}'
    else:
        message_text = f'Вы хотите посмотреть хотелки {command_split[1]}'
    await message.answer(message_text)


@command_router.message(F.forward_origin)
async def catch_forward(message: Message, bot: Bot):
    sender_name = message.forward_origin.sender_user.full_name
    sender_id = message.forward_origin.sender_user.id
    await bot.delete_message(
        message_id=message.message_id,
        chat_id=message.from_user.id,
    )
    message_text = f'Вы хотите посмотреть хотелки {sender_id}'
    await message.answer(message_text)


@command_router.message(Command('add'))
async def command_add(message: Message, bot: Bot):
    await message.answer('Слушаю внимательно!')
