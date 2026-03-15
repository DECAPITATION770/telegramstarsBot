from aiogram import Router

from handlers import start, stars
from middlewares.db import DbSessionMiddleware

router = Router()
router.message.middleware(DbSessionMiddleware())
router.include_router(start.router)
router.include_router(stars.router)
