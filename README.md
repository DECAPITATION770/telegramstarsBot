# Telegram-бот «Звёзды»

Бот для продажи звёзд. Пользователь вводит число в чат — бот списывает это количество звёзд. Если не хватает — сообщение «Недостаточно звёзд».

Данные хранятся в JSON-файле `data/users.json`.

## Требования

- Python 3.11+

## Docker

```bash
cp .env.example .env
# Заполните BOT_TOKEN, ADMIN_USERNAME, ADMIN_IDS в .env

docker compose up -d
```

Данные сохраняются в volume `bot_data`. Порт 8080 — бот.

## Установка (без Docker)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

1. Скопируйте `.env.example` в `.env`
2. Заполните переменные:
   - `BOT_TOKEN` — токен от @BotFather
   - `ADMIN_USERNAME` — username админа для кнопки «Связь с админом»
   - `ADMIN_IDS` — ID админов через запятую (например: `123456789,987654321`)

## Запуск

```bash
python main.py
```

Бот запустит aiohttp-сервер и будет принимать обновления по webhook на путь `/webhook`.

## Установка webhook вручную

Webhook устанавливается вручную через Telegram API:

```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-domain.com/webhook"
```

Замените `<BOT_TOKEN>` на токен бота и `https://your-domain.com` на публичный URL вашего сервера. Путь должен совпадать с `WEBHOOK_PATH` (по умолчанию `/webhook`).

Для локальной разработки можно использовать [ngrok](https://ngrok.com/):

```bash
ngrok http 8080
# Используйте выданный HTTPS-URL: https://xxxx.ngrok.io/webhook
```

## Render.com

1. Создай **Web Service** (Docker).
2. В Environment добавь: `BOT_TOKEN`, `ADMIN_USERNAME`, `ADMIN_IDS`, `WEB_SERVER_HOST=0.0.0.0`, `WEB_SERVER_PORT=8080`
3. Добавь **Disk** (persistent storage) и примонтируй к `/app/data` — там будет `users.json`
4. Webhook: `https://<your-service>.onrender.com/webhook`

**Важно:** без Disk данные теряются при перезапуске.

## Функционал

- `/start` — приветствие и кнопка «Связь с админом»
- Ввод числа — списание звёзд (при успехе: «Списано X звёзд», при нехватке: «Недостаточно звёзд»)

Баланс пользователей по умолчанию 0. Пополнение — редактирование `data/users.json` или будущие админ-команды.
