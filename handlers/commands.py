from aiogram import Bot, Router, F
from aiogram.types import Message, MessageEntity
from aiogram.filters import Command, CommandObject

from database import db
from keyboards import ikb_select_wish
import settings

command_router = Router()


# @command_router.message()
# async def catch_picture(message: Message, bot: Bot):
#     print(message.photo[-1].file_id)

@command_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject, bot: Bot):
    command_split = command.text.split(maxsplit=1)
    if len(command_split) == 1:
        target_user_id = message.from_user.id
    else:
        target_user_id = int(command_split[1])
    user_wishes = db.get_wishes(target_user_id)
    *_, description, photo, url = user_wishes[0]
    description = f'1/{len(user_wishes)}\n' + (description or '')
    photo = photo or settings.main_photo_id
    if url:
        description += f'\n\n{url}'
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=description,
        reply_markup=ikb_select_wish(
            user_tg_id=message.from_user.id,
            wishlist=user_wishes,
            current_id=0,
        )
    )


@command_router.message(Command('get_ref'))
async def get_referral_link(message: Message, bot: Bot):
    referral_link = f'https://t.me/stone_wishlist_bot?start={message.from_user.id}'
    await bot.send_message(
        chat_id=message.from_user.id,
        text=referral_link
    )


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


@command_router.message(Command('me'))
async def my_wishes(message: Message, bot: Bot):
    print(*user_wishes, sep='\n')


@command_router.message()
async def add_wish(message: Message, bot: Bot):
    user_id = message.from_user.id
    caption = message.text
    photo = None
    url = None
    if message.photo:
        caption = message.caption
        photo = message.photo[-1].file_id
    if message.entities or message.caption_entities:
        entities = message.caption_entities if photo else message.entities
        for item in entities:
            if item.type == 'url':
                url = item.extract_from(caption)
                caption = caption.replace(f'{url}', '').strip()
                break
    db.add_wish(user_id, caption, photo, url)
    await message.answer('Хотелка добавлена!')
