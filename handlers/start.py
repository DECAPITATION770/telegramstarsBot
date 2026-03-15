from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from config import ADMIN_USERNAME

router = Router()

START_TEXT = """<b>Обменяй звёзды на реальные деньги</b>

Хочешь вывести Telegram Stars в наличные? Мечтаешь монетизировать свои звёзды?

Просто введи число — сколько звёзд хочешь продать. Мы свяжемся с тобой."""


def get_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Связь с админом")]],
        resize_keyboard=True,
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if not message.from_user:
        return
    await message.answer(
        START_TEXT,
        reply_markup=get_reply_keyboard(),
    )


@router.message(F.text == "Связь с админом")
async def cmd_contact_admin(message: Message) -> None:
    if ADMIN_USERNAME:
        username = ADMIN_USERNAME.lstrip("@")
        await message.answer(
            f"Напишите нашему менеджеру: <a href=\"https://t.me/{username}\">@{username}</a>",
        )
    else:
        await message.answer("Связь с администратором временно недоступна.")
