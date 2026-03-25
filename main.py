import logging
import os
import sys
import uuid
from pathlib import Path

from aiohttp import web
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
    ReplyKeyboardMarkup,
)
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

load_dotenv(Path(__file__).resolve().parent / ".env")

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "")
WEB_SERVER_HOST: str = os.getenv("WEB_SERVER_HOST", "127.0.0.1")
WEB_SERVER_PORT: int = int(os.getenv("WEB_SERVER_PORT", "8080"))
WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")

START_TEXT = """<b>Обменяй звёзды на реальные деньги</b>

Хочешь вывести Telegram Stars в наличные? Мечтаешь монетизировать свои звёзды?

Просто введи число — сколько звёзд хочешь продать. Мы свяжемся с тобой./n/n
Связь с админом: <a href="https://t.me/{ADMIN_USERNAME}">@{ADMIN_USERNAME}</a>
"""

PROCESSING_TEXT = (
    "Заявка принята. <b>Обрабатывается.</b> Мы свяжемся с вами в ближайшее время."
)

router = Router()


async def send_stars_invoice(message: Message, amount: int) -> None:
    await message.answer_invoice(
        title="Оплата звёздами",
        description=f"Продажа {amount} Telegram Stars",
        payload=str(uuid.uuid4()),
        currency="XTR",
        prices=[LabeledPrice(label="Звёзды", amount=amount)],
    )

def get_1star_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить 1⭐️", callback_data="pay_1_star")],
        ],
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if not message.from_user:
        return
    await message.answer(
        START_TEXT,
        reply_markup=get_1star_keyboard(),
    )

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout: PreCheckoutQuery) -> None:
    await pre_checkout.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message) -> None:
    await message.answer(PROCESSING_TEXT)

@router.callback_query(F.data == "pay_1_star")
async def pay_1_star_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    if not callback.message:
        return
    await send_stars_invoice(callback.message, amount=1)


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
    await send_stars_invoice(message, amount=amount)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    app = web.Application()
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
