from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from sqlalchemy.future import select
from bot.init_bot import engine

from backend.models.Office import Office
from backend.models.QuizGroup import QuizGroup


async def get_values_from_query(query: Select):
    session = AsyncSession(engine, expire_on_commit=False)
    values = await session.execute(query)
    await session.close()
    return values.scalars().all()


async def get_value_from_query(query: Select):
    session = AsyncSession(engine, expire_on_commit=False)
    values = await session.execute(query)
    await session.close()
    return values.scalars().one()


async def check_office(message: Message) -> bool:
    offices = await get_values_from_query(select(Office))
    offices_name = [x.name for x in offices]
    return message.text not in offices_name


async def check_quiz_group(message: Message) -> bool:
    quizzes_groups = await get_values_from_query(select(QuizGroup))
    quizzes_groups_titles = [x.title for x in quizzes_groups]
    return message.text not in quizzes_groups_titles


def get_index_of_quiz(all_quizzes, quiz_query_id):
    index = -1
    for index, item in enumerate(all_quizzes):
        if item.id == quiz_query_id:
            break
        else:
            index = -1
    return index
