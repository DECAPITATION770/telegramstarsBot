# Telegram-бот «Звёзды»

Вся логика в одном файле **`main.py`**.

Бот принимает **Telegram Stars** — пользователь вводит число, получает счёт на оплату, платит звёздами через интерфейс Telegram.

## Как это работает

1. Пользователь вводит число (например, 5)
2. Бот отправляет счёт на 5 Telegram Stars
3. Пользователь нажимает «Оплатить» и списывает звёзды со своего аккаунта
4. После оплаты — сообщение о принятии заявки

Звёзды списываются напрямую через Telegram (как в @PremiumBot). Бот не хранит балансы.

## Требования

- Python 3.11+

## Установка

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

1. Скопируйте `.env.example` в `.env`
2. Заполните: `BOT_TOKEN`, `ADMIN_USERNAME`

## Запуск

```bash
python main.py
```

## Docker

```bash
cp .env.example .env
# Укажите BOT_TOKEN и ADMIN_USERNAME в .env

docker compose up -d --build
```

Внутри контейнера бот слушает `0.0.0.0:8080`; порт пробрасывается на хост (по умолчанию `8080`, см. `WEB_SERVER_PORT` в `.env` и в `docker-compose.yml`).

## Webhook

```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-domain.com/webhook"
```

Путь по умолчанию — `/webhook` (задаётся в `WEBHOOK_PATH` в `.env`).

## Функционал

- `/start` — приветствие и кнопка «Связь с админом»
- Ввод числа — счёт на оплату Telegram Stars
- После оплаты — подтверждение обработки заявки
