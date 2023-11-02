import aiohttp
from aiohttp import web
import asyncio
from aiogram import Bot, Dispatcher, types
import logging

bot = Bot(token="6509767694:AAEq0MTMGl3wo1vhbEJYdh_EUte1D5C0_k4")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

async def get_active_tasks():
    access_token = "v2f4npy3stjc2hrqzpoqkeha2ux5mve1"
    url = f"https://rz1101.bitrix24.ru/rest/task.item.list.json?filter={{'STATUS':2}}&select={{'ID'}}&auth={access_token}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if 'tasks' in data:
                return data['tasks']
            else:
                return []


async def get_task_data(task_id, access_token):
    url = f"https://rz1101.bitrix24.ru/rest/task.item.get.json?id={task_id}&auth={access_token}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data['result']


async def process_task_creation(filter_keywords):
    access_token = "v2f4npy3stjc2hrqzpoqkeha2ux5mve1"
    active_tasks = await get_active_tasks()
    print(f'Активные задачи: {active_tasks}')
    for task in active_tasks:
        task_id = task['ID']
        task_data = await get_task_data(task_id, access_token)
        task_title = task_data['title']

        print(f'Обработка задачи: {task_title}(ID:{task_id})')

        for keyword in filter_keywords:
            if keyword.lower() in task_title.lower():
                message = f"Новая задача: {task_title} (ID:{task_id})"
                chat_id = 1313756443
                await bot.send_message(chat_id, message)
                logging.info(message)


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher(bot)
    chat_id = 1313756443
    filter_keywords = ['Сервисная']
    await process_task_creation(filter_keywords,)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())







