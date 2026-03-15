# Telegram-бот «Звёзды»

Бот принимает **Telegram Stars** — пользователь вводит число, получает счёт на оплату, платит звёздами через интерфейс Telegram.

## Как это работает

1. Пользователь вводит число (например, 5)
2. Бот отправляет счёт на 5 Telegram Stars
3. Пользователь нажимает «Оплатить» и списывает звёзды со своего аккаунта
4. После оплаты — подтверждение «Списано X звёзд»

Звёзды списываются напрямую через Telegram (как в @PremiumBot). Бот не хранит балансы.

## Требования

- Python 3.11+

## Docker

```bash
cp .env.example .env
# Заполните BOT_TOKEN, ADMIN_USERNAME, ADMIN_IDS в .env

docker compose up -d
```

## Установка (без Docker)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

1. Скопируйте `.env.example` в `.env`
2. Заполните: `BOT_TOKEN`, `ADMIN_USERNAME`, `ADMIN_IDS`

## Запуск

```bash
python main.py
```

## Webhook

```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-domain.com/webhook"
```

## Функционал

- `/start` — приветствие и кнопка «Связь с админом»
- Ввод числа — счёт на оплату Telegram Stars
- После оплаты — «Списано X звёзд. Спасибо!»
