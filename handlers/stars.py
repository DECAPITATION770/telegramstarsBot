from aiogram import Router
from aiogram.types import Message

from database.storage import storage

router = Router()


@router.message(lambda m: m.text and m.text.isdigit())
async def handle_stars(message: Message) -> None:
    if not message.from_user:
        return
    user_id = message.from_user.id
    amount = int(message.text)
    if amount <= 0:
        await message.answer("Введите положительное число.")
        return
    success = await storage.deduct_stars(user_id, amount)
    if success:
        await message.answer(f"Списано {amount} звёзд.")
    else:
        await message.answer("Недостаточно звёзд.")
