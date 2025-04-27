
import os
import json
import logging
from typing import Optional

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.services.media import make_image
from bot.services.scoring import calc_scores, get_totem_animal

router = Router()
logger = logging.getLogger("zoobot.result")

ANIMALS_PATH = os.path.join("data", "animals.json")
with open(ANIMALS_PATH, encoding="utf-8") as f:
    ANIMALS = json.load(f)


async def show_result(message: types.Message, state: FSMContext):

    data = await state.get_data()
    answers = data.get("answers", [])

    scores = calc_scores(answers)
    top = get_totem_animal(scores)
    if top is None:
        await message.answer("Увы, Ваш тотем не определен, попробуйте ещё раз.")
        await state.clear()
        return

    totem_animal_key, totem_animal_score = top
    animal = ANIMALS.get(totem_animal_key)
    if not animal:
        logger.error(f"totem_animal key '{totem_animal_key}' отсутствует в animals.json")
        await message.answer("Что-то пошло не так... Нам жаль")
        await state.clear()
        return

    logger.info(f"Пользователь с id={message.from_user.id} — тотем: {animal['name']} ({totem_animal_score} очков)")

    image_path: Optional[str]
    try:
        image_path = await make_image(
            image_path=animal["image"],
            animal_name=animal["name"],
            user_name=message.from_user.first_name
        )
    except Exception:
        logger.exception("Ошибка при создании итоговой картинки")
        image_path = None

    caption = (
        f"🎉 *Ваше тотемное животное — {animal['name']}!*\n\n"
        f"_{animal['description']}_\n\n"
        f"[Не оставьте родственные души без опеки]({animal['guardian_link']})"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Попробовать еще раз", callback_data="start_quiz")],
        [InlineKeyboardButton(text="Поделиться", callback_data=f"share_{totem_animal_key}")],
        [InlineKeyboardButton(text="Оставить отзыв", callback_data="feedback")],
        [InlineKeyboardButton(text="Связаться с зоопарком", callback_data=f"contact_{totem_animal_key}")]
    ])

    if image_path:
        await message.answer_photo(
            photo=types.FSInputFile(image_path),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=kb
        )
    else:
        await message.answer(caption, parse_mode="Markdown", reply_markup=kb)

    await state.clear()
