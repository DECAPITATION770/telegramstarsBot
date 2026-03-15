from aiogram import Router

from handlers import start, stars

router = Router()
router.include_router(start.router)
router.include_router(stars.router)
