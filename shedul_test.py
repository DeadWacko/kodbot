from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import token
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
import json
from datetime import datetime
import sqlite3
jobstores = {
  'mongo': MongoDBJobStore(),
  'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}


job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = AsyncIOScheduler(jobstores=jobstores,  job_defaults=job_defaults)



bot = Bot(token=token)
dp = Dispatcher(bot)






#функция отправки сообщения
@dp.message_handler()
async def echo_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)



#функция проверки текущего времени

async def check_send_time():
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        day_naw = datetime.today().weekday()
        for user_id in json_data["jedi"]:
            for group in json_data["jedi"][user_id]["padawans_groups"]:
                lesson_day = json_data["jedi"][user_id]["padawans_groups"][group]["group_data"]["lesson_day"]
                lesson_time = json_data["jedi"][user_id]["padawans_groups"][group]["group_data"]["lesson_time"]
                lesson_number = json_data["jedi"][user_id]["padawans_groups"][group]["group_data"]["number_last_lesson"]
                lesson_time.split(':')
                lesson_hours = int(lesson_time[0])
                lesson_minutes = int(lesson_time[1])

                if int(lesson_day) >= day_naw:
                    if lesson_hours >= datetime.now().time().hour:
                        scheduler.add_job(echo_message, "date",
                                          next_run_time=datetime(2022, 1, 16, 2, 53),
                                          args=(397584737, "У тебя сегодня урок в группе,не забудь"))


def main():
    scheduler.add_job(echo_message, "interval", seconds=5,args=(397584737, "У тебя сегодня урок в группе,не забудь"))



def test():
    with open('data.JSON', 'r', encoding="utf-8") as f:
        json_data = json.load(f)
        day_naw = datetime.today().weekday()
        for user_id in json_data["jedi"]:
            for group in json_data["jedi"][user_id]["padawans_groups"]:
                lesson_day = json_data["jedi"][user_id]["padawans_groups"][group]["group_data"]["lesson_day"]
                lesson_time = json_data["jedi"][user_id]["padawans_groups"][group]["group_data"]["lesson_time"]
                lesson_number = json_data["jedi"][user_id]["padawans_groups"][group]["group_data"]["number_last_lesson"]
                lesson_time.split(':')
                lesson_hours = int(lesson_time[0])
                lesson_minutes = int(lesson_time[1])


                if int(lesson_day) >= day_naw:
                    if lesson_hours >= datetime.now().time().hour:
                        scheduler.add_job(echo_message, "date", next_run_time=datetime(2022,datetime.now().month,datetime.now().day,datetime.now().time().hour,lesson_minutes),
                                          args=("ne_katia", "У тебя сегодня урок в группе,не забудь"))














if __name__ == '__main__':
    main()
    scheduler.start()
    executor.start_polling(dp)
