import logging
import os

from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
logger = logging.getLogger("zoobot.feedback")

class Feedback(StatesGroup):
    waiting_for_text = State()

@router.callback_query(F.data == "feedback")
async def start_feedback(callback: types.CallbackQuery, state: FSMContext):
    logger.info(f"Пользователь {callback.from_user.id} запросил отзыв")
    await callback.message.answer(
        "Поделитесь вашими впечатлениями:"
    )
    await state.set_state(Feedback.waiting_for_text)
    await callback.answer()

@router.message(Feedback.waiting_for_text)
async def receive_feedback(message: types.Message, state: FSMContext):
    user = message.from_user
    text = message.text.strip()

    feedback_dir = "data"
    os.makedirs(feedback_dir, exist_ok=True)
    feedback_path = os.path.join(feedback_dir, "feedback.txt")

    try:
        with open(feedback_path, "a", encoding="utf-8") as f:
            f.write(f"{user.id} (@{user.username or user.first_name}): {text}\n")
        logger.info(f"Отзыв от {user.id} сохранён")
        await message.answer("Спасибо за Ваше мнение!")
    except Exception as e:
        logger.exception("Ошибка во время сохранения отзыва")
        await message.answer("Не удалось сохранить отзыв. Попробуйте позже.")

    await state.clear()
