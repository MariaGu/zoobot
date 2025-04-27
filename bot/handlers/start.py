import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
logger = logging.getLogger("zoobot.start")

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    logger.info(f"Пользователь с id={user.id} (@{user.username or user.full_name}) нажал /start")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поехали!", callback_data="start_quiz")]
    ])
    await message.answer(
        "Здравствуйте! Здесь Вы можете определить Ваше тотемное животное \nНачнем сейчас?",
        reply_markup=kb
    )
