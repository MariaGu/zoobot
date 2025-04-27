import logging
from aiogram import types

logger = logging.getLogger("zoobot.sharing")

async def share_result(message: types.Message, totem_animal_key: str, user_name: str):
    bot_username = "ZooMoscowTotemBot"
    bot_mention = f"@{bot_username.lstrip('@')}"

    text = (
        f"Привет, {user_name}! Я прошёл викторину от Московского зоопарка "
        f"и узнал, что моё тотемное животное — *{totem_animal_key}*!\n\n"
        f"Желаете узнать, кто Вы? → {bot_mention}\n\n"
        f"Пройдите и Вы {bot_mention}"
    )

    logger.info(f"share_result: user_id={message.from_user.id}, totem_animal={totem_animal_key}")
    await message.answer(text, parse_mode="Markdown")