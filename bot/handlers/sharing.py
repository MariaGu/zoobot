
import logging
from aiogram import Router, types, F

from bot.services.sharing import share_result

router = Router()
logger = logging.getLogger("zoobot.sharing")

@router.callback_query(F.data.startswith("share_"))
async def share_callback(callback: types.CallbackQuery):
    totem_animal_key = callback.data.replace("share_", "")

    user = callback.from_user

    user_name = user.first_name or user.username or str(user.id)
    logger.info(f"Пользователь с id={user.id} поделился результатом: {totem_animal_key}")
    await share_result(callback.message, totem_animal_key, user_name)
    await callback.answer()