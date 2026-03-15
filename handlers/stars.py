import uuid

from aiogram import Router, F
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

router = Router()


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout: PreCheckoutQuery) -> None:
    await pre_checkout.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message) -> None:
    amount = message.successful_payment.total_amount
    await message.answer(f"Списано {amount} звёзд. Спасибо!")


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
    payload = str(uuid.uuid4())
    await message.answer_invoice(
        title="Оплата звёздами",
        description=f"Оплата {amount} Telegram Stars",
        payload=payload,
        currency="XTR",
        prices=[LabeledPrice(label="Звёзды", amount=amount)],
    )
