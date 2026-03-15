from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import ADMIN_USERNAME
from database.storage import storage

router = Router()

START_TEXT = "Этот бот позволяет продавать звёздочки. Достаточно ввести число в чат."


def get_admin_keyboard() -> InlineKeyboardMarkup | None:
    if ADMIN_USERNAME:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Связь с админом",
                        url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}",
                    )
                ]
            ]
        )
    return None


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if not message.from_user:
        return
    user_id = message.from_user.id
    await storage.get_or_create_user(user_id)
    keyboard = get_admin_keyboard()
    await message.answer(
        START_TEXT,
        reply_markup=keyboard,
    )
