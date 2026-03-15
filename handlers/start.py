from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import ADMIN_USERNAME
from database.repositories import get_or_create_user

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
async def cmd_start(message: Message, session) -> None:
    if not message.from_user:
        return
    user_id = message.from_user.id
    await get_or_create_user(session, user_id)
    keyboard = get_admin_keyboard()
    await message.answer(
        START_TEXT,
        reply_markup=keyboard,
    )
