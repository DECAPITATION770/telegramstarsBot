from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def get_or_create_user(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(id=user_id, stars=0)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def deduct_stars(session: AsyncSession, user_id: int, amount: int) -> bool:
    result = await session.execute(
        update(User)
        .where(User.id == user_id, User.stars >= amount)
        .values(stars=User.stars - amount)
    )
    if result.rowcount > 0:
        await session.commit()
        return True
    return False
