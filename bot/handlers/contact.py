import os
import logging

from aiogram import Router, types, F

router = Router()
logger = logging.getLogger("zoobot.contact")

@router.callback_query(F.data.startswith("contact_"))
async def contact_user(callback: types.CallbackQuery):
    totem_animal_key = callback.data.replace("contact_", "")
    user = callback.from_user

    staff_info = (
        "Новый  запрос:\n"
        f"Пользователь: @{user.username or user.full_name} (ID: {user.id})\n"
        f"Животное: {totem_animal_key}\n"
    )

    try:
        os.makedirs("data", exist_ok=True)
        contact_path = os.path.join("data", "contact_requests.txt")
        with open(contact_path, "a", encoding="utf-8") as f:
            f.write(staff_info + "\n")
        logger.info(f"Contact request saved: user_id={user.id}, totem_animal={totem_animal_key}")
    except Exception:
        logger.exception("Ошибка при сохранении контактного запроса")

    await callback.message.answer(
        "Ваш запрос принят! Мы свяжемся с вами в ближайшее время."
    )
    await callback.answer()
