from aiogram import Router
from aiogram.types import Message

router = Router()

PROCESSING_TEXT = "Заявка принята. <b>Обрабатывается.</b> Мы свяжемся с вами в ближайшее время."


@router.message(lambda m: m.text and m.text.isdigit())
async def handle_stars(message: Message) -> None:
    if not message.from_user:
        return
    amount = int(message.text)
    if amount <= 0:
        await message.answer("Введите положительное число.")
        return
    if amount > 10000:
        await message.answer("Максимум 10000 звёзд за раз.")
        return
    await message.answer(PROCESSING_TEXT)
