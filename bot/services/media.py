import os
import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger("zoobot.media")

async def make_image(
    image_path: str,
    animal_name: str,
    user_name: str
) -> str:

    try:
        base = Image.open(image_path).convert("RGBA")
    except Exception:
        logger.exception(f"Не получается открыть изображение {image_path}")
        raise

    draw = ImageDraw.Draw(base)
    margin = 20

    fonts_dir       = "media/fonts"
    bold_path       = os.path.join(fonts_dir, "ALS_Story_2.0_B.otf")
    regular_path    = os.path.join(fonts_dir, "ALS_Story_2.0_R.otf")

    try:
        font_bold = ImageFont.truetype(bold_path, 48)
    except Exception:
        logger.warning(f"Не удалось загрузить шрифт {bold_path}, используем дефолт")
        font_bold = ImageFont.load_default()

    try:
        font_regular = ImageFont.truetype(regular_path, 36)
    except Exception:
        logger.warning(f"Не удалось загрузить шрифт {regular_path}, используем дефолт")
        font_regular = ImageFont.load_default()

    draw.text((margin, margin), animal_name, font=font_bold, fill="white")

    caption = f"{user_name}, это Ваше Тотемное животное!"

    logo_path = "media/logo/MZoo-logo-ßircle-mono-white-preview.jpg"
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_width = base.width // 5

            logo = logo.resize(
                (logo_width, int(logo_width * logo.height / logo.width))            )
            pos = (base.width - logo.width - margin, base.height - logo.height - margin)
            base.alpha_composite(logo, dest=pos)
        except Exception:
            logger.exception(f"Не получилось вставить логотип {logo_path}")
    else:
        logger.warning(f"Логотип не был найден по пути {logo_path}")

    out_dir = "media/generated"
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{user_name}_{animal_name}.png"
    output_path = os.path.join(out_dir, filename)
    try:
        base.save(output_path)
        logger.info(f"Получена картинка результата: {output_path}")
    except Exception:
        logger.exception(f"Не получилось сохранить изображение {output_path}")
        raise

    return output_path
